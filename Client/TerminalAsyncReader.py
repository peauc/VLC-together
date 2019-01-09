import fileinput
import sys
from threading import Thread, Lock


class TerminalAsyncReader(Thread):
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

    def run(self):
        while 1:
            array = [l for l in sys.stdin.read().splitlines() if l]
            if array:
                with self._lock:
                    self._command_queue += array

    def is_data_available(self):
        return bool(self._command_queue)
