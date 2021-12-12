import copy
import logging
import itertools
import socket
import select

from typing import Generator, Iterator

import common.network.Protobuff.Generated.packet_pb2 as packet_pb2
from server.src.CommandInterpreter import CommandInterpreter, CommandResponse
from server.src.constants import Constants
from server.src.Session import Session


class Server:

# TODO: Verify that the protobuff has been made
    def __init__(self):
        self.__current_users: [Session] = []
        self.__message_queue = {}
        self.__should_run = True
        self.__command_interpreter = CommandInterpreter()
        self.__setup_tcp_socket()

    def __setup_tcp_socket(self, ip=Constants.IP, port=Constants.PORT,
                           backlog=Constants.SOCKET_BACKLOG) -> None:
        """Setup a tcp socket and bind it to values defined server/src/constants.py."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind((ip, port))
        logging.debug(f"Bound {ip}:{port}")
        server.listen(backlog)
        self.__bound_socket = server

    def __accept_new_user(self, s: socket.socket) -> Session:
        """Accept a new user waiting on the socket."""
        connection, client_address = s.accept()
        print(f'New connection from {client_address}')
        connection.setblocking(False)
        new_user = Session(connection)
        self.__current_users.append(new_user)
        return new_user

    def handle_sockets(self, readable, writable, exceptional):
        """Handle operations on the socket."""
        for session in readable:
            data = session.sock.recv(Constants.SOCKET_PACKET_READ)
            if data:
                packet = packet_pb2.defaultPacket()
                packet.ParseFromString(data)
                self.handle_packets(session, packet)
            else:
                self.__remove_user(session)

        for session in writable:
            for message in session.output_queue:
                serialized_packet = message.SerializeToString()
                session.sock.send(serialized_packet)
            session.output_queue.clear()

        for session in exceptional:
            logging.error(f"handling exceptional conditions for {session.sock.getpeername()}")
            self.__remove_user(session)

    def check_for_new_connections(self):
        """Check for new connections waiting."""
        new_connections, _, __ = select.select([self.__bound_socket], [self.__bound_socket], [self.__bound_socket], 0)
        if not new_connections:
            return
        logging.debug(f'{len(new_connections)} new connections')
        for new_connection in new_connections:
            self.__accept_new_user(new_connection)

# TODO: We have to find a way to close client's connection and remove it from the client list
    def run(self) -> None:
        """Server mainloop.

        Handles new connections and inbound packets.
        """
        while self.__should_run:
            self.check_for_new_connections()
            input_sockets = copy.copy(self.__current_users)
            # Get the sockets from the current user
            output_sockets = list(self.__get_users_with_data_ready())
            readable, writable, exceptional = select.select(input_sockets, output_sockets,
                                                            itertools.chain(input_sockets, output_sockets), 0.5)

            self.handle_sockets(readable, writable, exceptional)

    def handle_packets(self, user: Session, packet: packet_pb2.defaultPacket):
        try:
            resp = self.__command_interpreter.interpret_command(user, packet)
            if resp == CommandResponse.SESSION_CLOSED:
                self.__remove_user(user)
        except AttributeError:
            logging.error(f"Received a corrupted packet from {user.sock.getpeername()}")

    def __get_users_with_data_ready(self) -> Iterator[Session]:
        return (user for user in self.__current_users if user.output_queue)

    def __remove_user(self, user):
        self.__current_users.remove(user)
        user.sock.close()
        user.output_queue.clear()




