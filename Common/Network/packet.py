from enum import Enum
import sys


class Commands(Enum):
    ERROR = -1
    JOIN = 0
    QUIT = 1
    VLC_COMMAND = 2
    SERVER_INFO = 3


class Packet:
    def __init__(self, command=Commands.ERROR, param=""):
        self.command_nb = command
        self.param = param

    def __str__(self):
        return f"Command {self.command_nb} with param :\"{self.param}\""
