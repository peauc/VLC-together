import logging
from vlc import VLC

class Player:
    def __init__(self):
        self.vlc = VLC()

    def add(self, filepath):
        self.vlc.add(filepath)

    def __pause(self):
        self.vlc.pause()

    def execute_command(self, string):
        if string.split(" ", 1)[0] in self.vlc.commands:
            logging.debug(string)
            self.vlc.x(string)
        else:
            logging.error(f"Command {string}, was not recognized")
            logging.debug(f"Command list {self.vlc.commands}")
