from constants import Constants
import socket
from Common.Network.packet import Packet


class Server:
    def __init__(self):
        self.__sockets = []

    def connect_to_default_ip(self):
        for ip, port in Constants.IP_TO_CONNECT_TO:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.sendall(bytes('add ../media/video.mp4'+'\n', 'utf-8'))
            self.__sockets.append(sock)
            # sock.sendall(bytes('stop' + '\n', 'utf-8'))

    def send_command(self, command: str):
        for sock in self.__sockets:
            if not command.endswith('\n'):
                command += '\n'
            sock.sendall(bytes(command, 'utf-8'))
