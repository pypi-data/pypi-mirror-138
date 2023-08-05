import threading


class TuningController:
    def __init__(self) -> None:
        self.lock = threading.Lock()

    def create_jobs(self):  # create job? get job?
        raise NotImplementedError()

    def validate_parameters(self):
        raise NotImplementedError()
