from Server.server import Server
import logging
import sys


def set_log():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    set_log()
    s = Server()
    s.run()


if __name__ == '__main__':
    main()
