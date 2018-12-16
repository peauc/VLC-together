import socket, select, sys, queue
from Common.Network.packet import Packet, Commands
import pickle

class Server:
    def __init__(self):
        self.__input = []
        self.__output = []
        self.__message_queue = {}

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind(('localhost', 8080))
        server.listen(5)
        self.__server = server
        self.__input.append(server)

    def run(self):
        while self.__input:
            readable, writable, exceptionnal = select.select(self.__input, self.__output, self.__input)
            for s in readable:
                if s is self.__server:
                    connection, client_address = s.accept()
                    print(f'New connection from {client_address}')
                    connection.setblocking(0)
                    self.__input.append(connection)
                    self.__message_queue[connection] = queue.Queue()
                else:
                    print(f"Size of a packet {sys.getsizeof(Packet())}")
                    data = s.recv(1048)
                    if data:
                        print(f"received \"{data}\" from {s.getpeername()}")
                        packet = pickle.loads(data)
                        print(f'Received a packet {packet}')
                        self.handle_packets(s, packet)
                    else:
                        print(f"Closing {s.getsockname()}")
                        if s in self.__output:
                            self.__output.remove(s)
                        self.__input.remove(s)
                        s.close()
                        del self.__message_queue[s]
            for s in writable:
                try:
                    next_message = self.__message_queue[s].get_nowait()
                except queue.Empty:
                    print(f"output queue for {s.getpeername()} is empty")
                    self.__output.remove(s)
                else:
                    print(f"sending {next_message} to {s.getpeername()}")
                    s.send(next_message)
            for s in exceptionnal:
                print(f"handling exceptionnal conditions for {s.getpeername()}")
                self.__input.remove(s)
                if s in self.__output:
                    self.__output.remove(s)
                s.close()
                del self.__message_queue[s]

    def handle_packets(self, s : socket.socket, packet : Packet):
        if packet.command_nb in Commands:

        pass
