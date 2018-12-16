import sys
import logging
import socket
import pickle
import time

from Common.Network.packet import Packet, Commands


def setup_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    setup_logging()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 8080))
        pack = Packet()
        pack.param = "Hello as tu pensé a a aller niquer ta emre "
        pack.command_nb = Commands.JOIN
        s.sendall(pickle.dumps(pack))
        time.sleep(1)


if __name__ == '__main__':
    main()
