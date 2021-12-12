import sys
from threading import Thread, Lock


class TerminalAsyncReader(Thread):
    @property
    def is_running(self):
        return self.__should_run

    @property
    def lock(self):
        return self._lock

    @property
    def command_queue(self):
        return self._command_queue

    def __init__(self):
        super(TerminalAsyncReader, self).__init__()
        self._lock = Lock()
        self._command_queue = []
        self.__should_run = True

    def stop(self):
        self.__should_run = False

    def run(self):
        while self.__should_run:
            array = [l for l in sys.stdin.read().splitlines() if l]
            if array:
                with self._lock:
                    self._command_queue += array

    def is_data_available(self):
        return bool(self._command_queue)
