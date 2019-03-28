import Common.Network.Protobuff.Generated.packet_pb2 as packet_pb2
import logging
import socket, select
from Server.src.CommandInterpreter import CommandInterpreter, CommandResponse
from Server.src.constants import Constants
from Server.src.User import User


class Server:

# TODO: Verify that the protobuff has been made
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
        new_user = User(connection)
        self.__current_users.append(new_user)

    # TODO: We have to find a way to close client's connection and remove it from the client list
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
                        packet = packet_pb2.defaultPacket()
                        packet.ParseFromString(data)
                        self.handle_packets(user, packet)
                    else:
                        self.__remove_user(user)

            for user in writable:
                for message in user.output_queue:
                    serialized_packet = message.SerializeToString()
                    user.sock.send(serialized_packet)
                user.output_queue.clear()

            for user in exceptional:
                logging.error(f"handling exceptional conditions for {user.sock.getpeername()}")
                self.__remove_user(user)

    def handle_packets(self, user: User, packet: packet_pb2.defaultPacket):
        try:
            resp = self.__command_interpreter.interpret_command(user, packet)
            if resp == CommandResponse.SESSION_CLOSED:
                self.__remove_user(user)
        except AttributeError:
            logging.error(f"Received a corrupted packet from {user.sock.getpeername()}")

    def __get_users_with_data_ready(self) -> [User]:
        users = []
        for user in self.__current_users:
            if user.output_queue:
                users.append(user)
        return users

    def __remove_user(self, user):
        self.__current_users = [f for f in self.__current_users if user != f]
        user.sock.close()

        # We clear the client's output queue without looking if there still is information inside
        user.output_queue.clear()


