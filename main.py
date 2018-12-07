import sys
import logging
from vlc import VLC

from constants import Constants
from player import Player

def setup_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
    setup_logging()
    player = Player()

    while 1:
        command = input(">")
        player.execute_command(command)

if __name__ == '__main__':
    main()
