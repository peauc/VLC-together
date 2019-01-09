import socket, select, sys, queue
from Server.CommandInterpreter import CommandInterpreter
from Common.Network.packet import Packet
from Server.constants import Constants
from Server.User import User
import pickle


class Server:
    def __init__(self):
        self.__output = []
        self.__current_users = []
        self.__message_queue = {}
        self.__command_interpreter = CommandInterpreter()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind((Constants.IP, Constants.PORT))
        server.listen(5)
        self.__server = server

    def poll_server(self, s: socket.socket):
        connection, client_address = s.accept()
        print(f'New connection from {client_address}')
        connection.setblocking(0)
        self.__current_users.append(User(connection))
        self.__message_queue[connection] = queue.Queue()

    def run(self):
        while 1:
            # Get the sockets from the current user
            sockets = self.__current_users + [self.__server]
            readable, writable, exceptionnal = select.select(sockets, self.__output, sockets)
            for user in readable:
                if user is self.__server:
                    self.poll_server(user)
                else:
                    data = user.sock.recv(1048)
                    if data:
                        print(f"received \"{data}\" from {user.sock.getpeername()}")
                        packet = pickle.loads(data)
                        print(f'Received a packet {packet}')
                        self.handle_packets(user, packet)
                    else:
                        print(f"Closing {user.getsockname()}")
                        if user in self.__output:
                            self.__output.remove(user)
                        self.__current_users = [f for f in self.__current_users if user != f]
                        user.sock.close()
                        del self.__message_queue[user]
            for user in writable:
                try:
                    next_message = self.__message_queue[user].get_nowait()
                except queue.Empty:
                    print(f"output queue for {user.sock.getpeername()} is empty")
                    self.__output.remove(user)
                else:
                    print(f"sending {next_message} to {user.sock.getpeername()}")
                    user.sock.send(next_message)
            for user in exceptionnal:
                print(f"handling exceptionnal conditions for {user.sock.getpeername()}")
                self.__current_users = [f for f in self.__current_users if user != f.sock]
                if user in self.__output:
                    self.__output.remove(user)
                user.close()
                del self.__message_queue[user]

    def handle_packets(self, user: User, packet : Packet):
        self.__command_interpreter.interpret_command(user, packet)

