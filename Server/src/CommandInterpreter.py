import Common.Network.Protobuff.Generated.packet_pb2 as packet_pb2
import Common.Utils.network as network_utils
import logging
from .RoomHandler import RoomHandler
from .User import User
from enum import Enum


class CommandResponse(Enum):
    PARAM_ERROR = -1
    OK = 0


class CommandInterpreter:
    def __init__(self):
        self.__room_handler = RoomHandler()
        self.__command_list = {
            packet_pb2.defaultPacket.ERROR: self._error,
            packet_pb2.defaultPacket.JOIN: self._join,
            packet_pb2.defaultPacket.VLC_COMMAND: self._vlc_command,
            packet_pb2.defaultPacket.QUIT: self._quit
        }

    @property
    def accepted_commands(self):
        return [k for k, v in self.__command_list]

    def _error(self, user: User, packet_string: str):
        pass

    def _join(self, user: User, packet_string: str):
        split_param = packet_string.split(' ')
        if len(split_param) < 1 or len(split_param) > 2:
            return CommandResponse.PARAM_ERROR, "join parameters error\njoin room_name [room_password]\n"
        self.__room_handler.add_user_to_room(user, *split_param)
        # Maybe add a nickname for users
        room_message = network_utils.create_packet(packet_pb2.defaultPacket.SERVER_INFO, f"A new user {user.sock.getpeername()} has joined")
        user.add_to_output_queue(room_message)
        # The room name is guarenteed
        logging.debug(f"User {user} joined the room {split_param[0]}")
        return CommandResponse.OK, ""

    def _quit(self, user: User, packet_string: str):
        room = self.__room_handler.get_room_from_user(user)
        if room is not None:
            packet = network_utils.create_packet(packet_pb2.defaultPacket.SERVER_INFO, f"User {user} left with message {packet_string}")
            room.send_packet_to_users(packet)
        self.remove_user_trace(user)
        logging.debug(f"user {user} is leaving")
        user.output_queue.clear()
        user.sock.close()
        return CommandResponse.OK, "Session closed"

    def _vlc_command(self, user: User, packet_string: str):
        room = self.__room_handler.get_room_from_user(user)
        if room is not None:
            packet = network_utils.create_packet(packet_pb2.defaultPacket.VLC_COMMAND, packet_string)
            logging.debug(f"user [{user}] is sending command [{packet_string}] to room: [{room}]")
            room.send_packet_to_users(packet)
        return CommandResponse.OK, ""

    def remove_user_trace(self, user: User):
        room = self.__room_handler.get_room_from_user(user)
        if room is not None:
            self.__room_handler.remove_user_from_room(user, room)

    def interpret_command(self, user: User, packet: packet_pb2.defaultPacket):
        descriptor = packet_pb2.defaultPacket.Commands.DESCRIPTOR

        if packet.command in descriptor.values_by_number:
            response, info = self.__command_list[packet.command](user, packet.param)
            if response == CommandResponse.PARAM_ERROR:
                message = network_utils.create_packet(packet_pb2.defaultPacket.ERROR, info)
                user.add_to_output_queue(message)
