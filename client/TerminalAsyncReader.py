import sys
import threading


class TerminalAsyncReader(threading.Thread):
    def __init__(self):
        super(TerminalAsyncReader, self).__init__()
        self._lock = threading.Lock()
        self._command_queue = []
        self.__should_run = True

    @property
    def is_running(self):
        return self.__should_run

    @property
    def lock(self):
        return self._lock

    @property
    def command_queue(self):
        return self._command_queue

    def stop(self):
        self.__should_run = False

    def run(self):
        while self.__should_run:
            lines = input().splitlines()
            if not lines:
                continue
            with self._lock:
                self._command_queue += lines

    def is_data_available(self):
        return bool(self._command_queue)
