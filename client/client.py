import logging
import select
import os
import time
import common.network.Protobuff.Generated.packet_pb2 as packet_pb2
from .constants import Constants
from .UserInputHandler import UserInputHandler
from .ServerConnection import ServerConnection
from client.vlc import VLC


class Client:
    """Client for VLCTogether."""
    def __init__(self, ip=None, port=None):
        self.vlc = VLC()
        self.ip = ip
        self.port = port
        # TODO Remove and use argparse
        self.ip = Constants.IP
        self.port = Constants.PORT
        self.__server = ServerConnection(self.ip, self.port)
        self.__uih = UserInputHandler()

    def run(self):
        """Client's mainloop."""
        logging.debug(f"Current directory {os.getcwd()}")
        # TODO: Give the client a way to quit gracefully
        while self.__uih.should_run():
            self.send_user_inputs()
            self.handle_networking()

    def send_user_inputs(self):
        """."""
        packets = self.__uih.read_and_serialize_user_input()
        if packets:
            for packet in packets:
                self.__server.queue_to_send(packet)

    def handle_networking(self):
        """Handle the networking for the client.

        Receive and send packets.
        """
        # If the server need to send back information we append his socket to the list so it can be polled by select
        r, w, e = select.select([self.__server], [self.__server], [self.__server], 0.5)

        for socket in r:
            data = socket.socket.recv(Constants.SOCKET_PACKET_READ)
            if data:
                packet = packet_pb2.defaultPacket()
                packet.ParseFromString(data)
                self.vlc.x(packet.param)
            else:
                logging.debug(f"0 byte read")

        for socket in w:
            for packet in socket.output_queue:
                serialized_data = packet.SerializeToString()
                socket.socket.send(serialized_data)
            socket.output_queue.clear()

        for socket in e:
            logging.error(f"handling exceptionnal conditions for {socket.sock.getpeername()}")
            socket.close()
            logging.error(f"Connection to remote host was closed")
            exit(1)
