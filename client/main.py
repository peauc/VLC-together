import sys
import logging

from player import Player


def setup_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    setup_logging()
    player = Player()


if __name__ == '__main__':
    main()
