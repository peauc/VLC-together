import sys
import logging
import socket
import pickle
import time
from Client.CommandInterpreter import CommandInterpreter
from Common.Network.packet import Packet, Commands


def setup_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def get_connection_infos():
    ip = input("Please input connection Ip")
    port = input("Please enter connection port")
    return ip, port


def main():
    setup_logging()
    # ip, port = get_connection_infos()
    # TODO: Remove temporary placeholder
    ip = 'localhost'

    port = 8080
    ci = CommandInterpreter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    while 1:
        packets = ci.parse_and_execute_commands()
        if packets:
            for packet in packets:
                print(packet)
                sock.sendall(pickle.dumps(packet))


if __name__ == '__main__':
    main()
