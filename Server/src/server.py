import logging
import socket, select
from Server.src.CommandInterpreter import CommandInterpreter
from Common.Network.packet import Packet
from Server.src.constants import Constants
from Server.src.User import User
import pickle


class Server:

    def __init__(self):
        self.__current_users = []
        self.__message_queue = {}
        self.__should_run = True
        self.__command_interpreter = CommandInterpreter()
        self.__server = self.__setup_server()

    def __setup_server(self) -> socket.socket:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind((Constants.IP, Constants.PORT))
        logging.debug(f"Listening on {Constants.IP}:{Constants.PORT}")
        server.listen(5)
        return server

    def accept_new_user(self, s: socket.socket):
        connection, client_address = s.accept()
        print(f'New connection from {client_address}')
        connection.setblocking(False)
        self.__current_users.append(User(connection))

    def run(self):
        while self.__should_run:
            input_sockets = self.__current_users + [self.__server]
            # Get the sockets from the current user
            output_sockets = self.__get_users_with_data_ready()
            readable, writable, exceptional = select.select(input_sockets, output_sockets, input_sockets)

            for user in readable:
                if user is self.__server:
                    self.accept_new_user(user)
                else:
                    data = user.sock.recv(1048)
                    if data:
                        self.handle_packets(user, pickle.loads(data))
                    else:
                        self.__remove_user(user)

            for user in writable:
                for message in user.output_queue:
                    logging.info(f"sending {message} to {user.sock.getpeername()}")
                    user.sock.send(pickle.dumps(message))
                user.output_queue.clear()

            for user in exceptional:
                logging.error(f"handling exceptional conditions for {user.sock.getpeername()}")
                self.__remove_user(user)

    def handle_packets(self, user: User, packet: Packet):
        try:
            self.__command_interpreter.interpret_command(user, packet)
        except AttributeError:
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


