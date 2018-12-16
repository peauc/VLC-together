from enum import Enum
import sys


class Commands(Enum):
    NONE = -1
    JOIN = 0
    QUIT = 1
    SAY = 2
    VLC_COMMAND = 3


class Packet:
    def __init__(self):
        self.command_nb = Commands.NONE
        self.param = ''

    def __str__(self):
        return f"Command {self.command_nb} with param :\"{self.param}\""
