import os
import threading
import time
from typing import TYPE_CHECKING

import psutil
import pynvml

if TYPE_CHECKING:
    from manta_lab.sdk.interface.interface import Interface

# TODO: add vendor pandas?
# TODO: track gpu per process
# TODO: add thread

# WARNING: DO NOT CHANGE THIS VALUE, SERVER WILL BLOCK YOUR REQUEST
DEBOUNCE_SECONDS = 1
FLUSHING_SAMPLE_COUNTS = 5

"""
TODO: how about initiating systemstat in run somewhere like on_init
"""


class SystemStats:
    def __init__(self, interface: "Interface", pid: int = None, method: str = "mean") -> None:
        try:
            pynvml.nvmlInit()
            self.gpu_count = pynvml.nvmlDeviceGetCount()
        except pynvml.NVMLError:
            self.gpu_count = 0

        self._pid = pid or os.getpid()
        self._interface = interface
        self._method = method

        self._shutdown = False
        self._thread = None
        self._buffer = {}
        self._sample_counts = 0
        net = psutil.net_io_counters()
        self.network_init = {"sent": net.bytes_sent, "recv": net.bytes_recv}

    @property
    def proc(self) -> psutil.Process:
        return psutil.Process(pid=self._pid)

    def start(self) -> None:
        if self._thread is None:
            self._shutdown = False
            self._thread = threading.Thread(target=self._thread_body)
            self._thread.name = "SystemStatsThread"
            self._thread.daemon = True

        if not self._thread.is_alive():
            self._thread.start()

    def shutdown(self) -> None:
        self._shutdown = True
        try:
            if self._thread is not None:
                self._thread.join()
        finally:
            self._thread = None

    def _flush(self) -> None:
        stats = self.get_current_stats()
        for stat, value in stats.items():
            if isinstance(value, (float, int)):
                samples = list(self._buffer.get(stat, [value]))
                stats[stat] = round(sum(samples) / len(samples), 2)

        self._interface.publish_stats(stats)
        self._sample_counts = 0
        self._buffer = {}

    def _thread_body(self) -> None:
        while True:
            # collect stats
            stats = self.get_current_stats()
            for stat, value in stats.items():
                if isinstance(value, (int, float)):
                    self._buffer[stat] = self._buffer.get(stat, [])
                    self._buffer[stat].append(value)
            self._sample_counts += 1

            # flush if shutdown or enough sample
            if self._shutdown or self._sample_counts >= FLUSHING_SAMPLE_COUNTS:
                self._flush()
                if self._shutdown:
                    break

            # debouncing
            # TODO: Do we need time spliting for fast shutdown?
            time.sleep(DEBOUNCE_SECONDS)

    def _get_gpu_stats(self, stats):
        # TODO: M1 GPU is different

        gpus_info = []
        for i in range(0, self.gpu_count):
            info = {}
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            try:
                utilz = pynvml.nvmlDeviceGetUtilizationRates(handle)
                memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

                info["gpu"] = utilz.gpu
                info["memory"] = utilz.memory
                info["memoryAllocated"] = (memory.used / float(memory.total)) * 100
                info["temp"] = temp

                try:
                    power_watts = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                    power_capacity_watts = pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000.0
                    power_usage = (power_watts / power_capacity_watts) * 100

                    info["powerWatts"] = power_watts
                    info["powerPercent"] = power_usage

                except pynvml.NVMLError:
                    pass

            except pynvml.NVMLError:
                pass

            gpus_info.append(info)

        stats["gpu"] = gpus_info

    def _get_basic_stats(self, stats):
        net = psutil.net_io_counters()
        sysmem = psutil.virtual_memory()
        stats["cpu"] = psutil.cpu_percent()
        stats["memory"] = sysmem.percent
        stats["network"] = {
            "sent": net.bytes_sent - self.network_init["sent"],
            "recv": net.bytes_recv - self.network_init["recv"],
        }
        # TODO: maybe show other partitions, will likely need user to configure
        stats["disk"] = psutil.disk_usage("/").percent

        process_info = {
            "memory": {
                "availableMB": sysmem.available / 1048576.0,
                "rssMB": 0,
                "percent": 0,
            },
            "cpu": {"threads": 0},
        }
        try:
            process_info["memory"]["rssMB"] = self.proc.memory_info().rss / 1048576.0
            process_info["memory"]["percent"] = self.proc.memory_percent()
            process_info["cpu"]["threads"] = self.proc.num_threads()
        except psutil.NoSuchProcess:
            pass
        stats["proc"] = process_info

    def _get_tpu_stats(self, stats):
        pass

    def get_current_stats(self):
        stats = dict()
        self._get_basic_stats(stats)
        self._get_gpu_stats(stats)
        self._get_tpu_stats(stats)
        return stats
