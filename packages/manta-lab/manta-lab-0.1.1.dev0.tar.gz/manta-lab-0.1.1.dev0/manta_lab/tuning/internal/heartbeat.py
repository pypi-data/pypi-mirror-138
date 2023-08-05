import threading


class SchedulerHeartbeat:
    def __init__(self) -> None:
        self._thread: threading.Thread

    def thread_body(self):
        pass
