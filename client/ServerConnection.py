import socket


class ServerConnection(object):
    @property
    def fileno(self):
        return self.socket.fileno

    def __init__(self, ip, port):
        self.output_queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.socket.setblocking(False)
        self.should_run = True

    def stop(self):
        """Stop the server."""
        self.should_run = False

    def __del__(self):
        self.socket.close()

    def queue_to_send(self, param):
        self.output_queue.append(param)

