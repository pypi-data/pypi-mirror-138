import collections
import itertools
import os
import queue
import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional, TYPE_CHECKING

import pandas as pd

import manta_lab as ml

if TYPE_CHECKING:
    from manta_lab.base.packet import ArtifactRequestPacket

Item = collections.namedtuple("Item", ("filename", "data"))
FinishItem = collections.namedtuple("FinishItem", ("exitcode"))
ArtifactItem = collections.namedtuple("ArtifactItem", ("data", "committed"))


class PusherBase:
    MAX_ITEMS_PER_PUSH = None

    def __init__(self, api, start_time=None):
        self.api = api
        self._start_time = start_time or time.time()

        self._queue = queue.Queue()
        self._thread = None

    @property
    def name(self):
        return self.__class__.__name__

    def _read_queue(self):
        wait_seconds = self._debounce_seconds()
        return ml.util.read_many_from_queue(self._queue, self.MAX_ITEMS_PER_PUSH, wait_seconds)

    def _debounce_seconds(self):
        raise NotImplementedError()

    def _thread_body(self):
        raise NotImplementedError()

    def start(self):
        # TODO: refactor with ./thread.py
        self._thread = threading.Thread(target=self._thread_body)
        self._thread.name = self.name
        self._thread.daemon = True
        self._thread.start()

    def push(self, file, data):
        raise NotImplementedError()

    def finish(self):
        """Cleans up.
        finish thread by add finish item in queue

        Arguments:
            exitcode: The exitcode of the watched process.
        """
        self._queue.put(FinishItem(0))  # TODO: feed exit code
        # TODO: cleaning
        print("waiting for finish item")
        self._thread.join()
        # TODO: show exception info


class LiveArtifactPusher(PusherBase):
    MAX_ITEMS_PER_PUSH = 10


class FilePusher(PusherBase):
    MAX_ITEMS_PER_PUSH = 8

    def _debounce_seconds(self):
        return 5

    def push(self, data):
        self._queue.put(data)

    def _thread_body(self):
        finished = None

        while finished is None:
            items = self._read_queue()
            for item in items:
                if isinstance(item, FinishItem):
                    print("finish item detected")
                    finished = item
                else:
                    if hasattr(item, "_manifest"):
                        print("item detected:", item._manifest.keys())

                    self._send_artifact(item)

    # TODO: need to consider we use item base stram or not
    def _send_artifact(self, artifact: "ArtifactRequestPacket") -> Optional[Dict]:
        saver = ml.sdk.ArtifactSaver(self.api)
        saver.save(artifact)


@dataclass
class StreamState:
    found_cr: bool = False
    cr: int = None
    last_offset: int = None


class RecordPusher(PusherBase):
    # WARNING: DO NOT CHANGE VALUES BELOW, API WILL REJECT YOUR REQUEST.
    HEARTBEAT_SECONDS = 30
    MAX_ITEMS_PER_PUSH = 10000

    def __init__(self, api, start_time=None):
        super().__init__(api=api, start_time=start_time)

        self.global_offset = 0
        self.stdout_state = StreamState()
        self.stderr_state = StreamState()

    def push(self, file, data):
        self._queue.put(Item(file, data))

    def _debounce_seconds(self):
        run_time = time.time() - self._start_time
        if run_time < 60:
            return self.HEARTBEAT_SECONDS / 15
        elif run_time < 300:
            return self.HEARTBEAT_SECONDS / 3
        else:
            return self.HEARTBEAT_SECONDS

    def _get_interval(self, len_data, target_num=50):
        # FIXME: this function should be covered by debouncing + something
        interval = len_data // target_num
        interval = max(interval, 1)
        return interval

    def _aggregate_items(self, items):
        res = []
        for item in items:
            res.append(item.data)
        return res

    def _aggregate_history_items(self, items):
        df = []
        for item in items:
            df.append(item.data)
        df = pd.DataFrame(df)

        x_axis_yn = df.columns.str.startswith("_")
        x_axis_cols = list(df.columns[x_axis_yn])
        y_axis_cols = list(df.columns[~x_axis_yn])
        output_cols = ["value"] + x_axis_cols

        res = {}
        for k in y_axis_cols:
            data_cols = [k] + x_axis_cols
            _d = df.loc[:, data_cols].dropna()
            _d.columns = output_cols
            _d = _d.to_dict(orient="records")
            res[k] = _d[:: self._get_interval(len(_d))]

        return res

    def _aggregate_log_items(self, items):
        # FIXME: this is temporal
        console = {}
        sep = os.linesep

        for item in items:
            lines = item.data["lines"]
            lines_str = "".join(lines)

            for line in lines:
                stream = getattr(self, f'{item.data["steam"]}_state')
                if line.startswith("\r"):
                    # starting with \r will overwrite console offset.
                    offset = stream.cr if stream.found_cr else stream.last_offset or 0
                    stream.cr = offset
                    stream.found_cr = True
                    console[offset] = {
                        "line": line[1:].strip() + "\n",
                        "_timestamp": item.data["_timestamp"],
                        "steam": item.data["steam"],
                    }

                    # lines_str = "\r progress bar\n" for progress bar updates.
                    # If instead lines_str = "\r progress bar\n text\n text\n",
                    # treat this as the end of a progress bar.
                    if lines_str.count(sep) > 1 and lines_str.replace(sep, "").count("\r") == 1:
                        stream.found_cr = False

                elif line and line != "\n":
                    console[self.global_offset] = {
                        "line": line.strip() + "\n",
                        "_timestamp": item.data["_timestamp"],
                        "steam": item.data["steam"],
                    }

                    stream.last_offset = self.global_offset
                    self.global_offset += 1

        res = list(console.values())
        return res

    def _aggregate_send(self, buffer):
        files = {}
        # Groupby needs group keys to be sorted
        buffer.sort(key=lambda c: c.filename)
        for filename, file_items in itertools.groupby(buffer, lambda c: c.filename):
            # TODO: this is temporal, find better way to handle it
            if filename == "histories":
                processed_items = self._aggregate_history_items(file_items)
            elif filename == "logs":
                processed_items = self._aggregate_log_items(file_items)
            else:
                processed_items = self._aggregate_items(file_items)

            files[filename] = processed_items

        self.api.send_run_record(**files)

    def _heartbeat_send(self):
        self.api.send_heartbeat()

    def _thread_body(self):
        buffer = []
        latest_post_time = time.time()
        latest_heartbeat_time = time.time()
        finished = None
        while finished is None:
            items = self._read_queue()
            for item in items:
                if isinstance(item, FinishItem):
                    print("finish item detected")
                    finished = item
                else:
                    buffer.append(item)

            cur_time = time.time()
            if buffer and cur_time - latest_post_time > self._debounce_seconds():
                latest_post_time = cur_time
                latest_heartbeat_time = cur_time
                self._aggregate_send(buffer)
                buffer = []

            # if stats are disabled, theres something we need to send heartbeat to server for tracking run status
            if cur_time - latest_heartbeat_time > self.HEARTBEAT_SECONDS:
                latest_heartbeat_time = cur_time
                self._heartbeat_send()

        # TODO: send api stream finished to server
        pass
