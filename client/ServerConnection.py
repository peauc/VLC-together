import socket


class ServerConnection(object):
    @property
    def socket(self):
        return self.__socket

    @property
    def output_queue(self):
        return self.__output_queue

    @property
    def should_run(self):
        return self.__should_run

    def __init__(self, ip, port):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((ip, port))
        self.__should_run = True
        self.__output_queue = []

    def __del__(self):
        self.__socket.close()

    def fileno(self):
        return self.__socket.fileno()

    def add_to_output_queue(self, param):
        self.__output_queue.append(param)

