import socket


class Session:
    def __init__(self, s: socket.socket):
        self.__socket = s
        self.__output_queue = []

    @property
    def sock(self):
        return self.__socket

    @property
    def output_queue(self):
        return self.__output_queue

    def add_to_output_queue(self, sentence):
        self.__output_queue.append(sentence)

    def fileno(self):
        return self.sock.fileno()
