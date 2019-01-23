import socket


class ServerConnection:
    def __init__(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        self.__output_queue = []
        self.__socket = sock
        pass

    @property
    def socket(self):
        return self.__socket

    @property
    def output_queue(self):
        return self.__output_queue

    def fileno(self):
        return self.__socket.fileno()

    def add_to_output_queue(self, param):
        self.__output_queue.append(param)
