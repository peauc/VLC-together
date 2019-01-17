import logging
import socket, select, sys, queue
from Server.CommandInterpreter import CommandInterpreter
from Common.Network.packet import Packet
from Server.constants import Constants
from Server.User import User
import pickle


class Server:
    def __init__(self):
        self.__current_users = []
        self.__message_queue = {}
        self.__command_interpreter = CommandInterpreter()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind((Constants.IP, Constants.PORT))
        server.listen(5)
        self.__server = server

    def accept_new_user(self, s: socket.socket):
        connection, client_address = s.accept()
        print(f'New connection from {client_address}')
        connection.setblocking(False)
        self.__current_users.append(User(connection))

    def run(self):
        while 1:
            # Get the sockets from the current user
            input_sockets = self.__current_users + [self.__server]
            output_sockets = self.__get_users_with_data_ready()
            readable, writable, exceptionnal = select.select(input_sockets, output_sockets, input_sockets)

            for user in readable:
                if user is self.__server:
                    self.accept_new_user(user)
                else:
                    data = user.sock.recv(1048)
                    if data:
                        packet = pickle.loads(data)
                        self.handle_packets(user, packet)
                    # If the select wake up and read on this socket but has no data,
                    # it means the connection is getting closed
                    else:
                        self.__remove_user(user)

            for user in writable:
                for message in user.output_queue:
                    logging.info(f"sending {message} to {user.sock.getpeername()}")
                    user.sock.send(pickle.dumps(message))
                user.output_queue.clear()

            for user in exceptionnal:
                logging.error(f"handling exceptionnal conditions for {user.sock.getpeername()}")
                self.__current_users = [f for f in self.__current_users if user != f]
                if user in output_sockets:
                    output_sockets.remove(user)
                user.close()

    def handle_packets(self, user: User, packet : Packet):
        try:
            self.__command_interpreter.interpret_command(user, packet)
        except AttributeError as e:
            logging.error(f"Recevied a corrupted packet from {user.sock.getpeername()}")

    def __get_users_with_data_ready(self) -> [User]:
        users = []
        for user in self.__current_users:
            if user.output_queue:
                users.append(user)
        return users

    def __remove_user(self, user):
        logging.info(f"Closing {user.sock.getsockname()}")
        self.__current_users = [f for f in self.__current_users if user != f]
        self.__command_interpreter.remove_user_trace(user)
        user.sock.close()

        # We clear the client's output queue without looking if there still is information inside
        user.output_queue.clear()

