import logging
from Common.Network.packet import Commands, Packet
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
            Commands.JOIN: self._join,
            Commands.VLC_COMMAND: self._vlc_command
        }

    @property
    def accepted_commands(self):
        return [k for k, v in self.__command_list]

    def _join(self, user: User, packet_string: str):
        splited_param = packet_string.split(' ')
        if len(splited_param) < 1 or len(splited_param) > 2:
            return CommandResponse.PARAM_ERROR, "join parameters error\njoin room_name [room_password]\n"
        self.__room_handler.add_user_to_room(user, *splited_param)
        # Maybe add a nickname for users
        user.add_to_output_queue(Packet(Commands.SERVER_INFO, f"A new user {user.sock.getpeername()} has joined"))
        return CommandResponse.OK, ""

    def _vlc_command(self, user: User, packet_string: str):
        room = self.__room_handler.get_room_from_user(user)
        if room is not None:
            packet = Packet(Commands.VLC_COMMAND, packet_string)
            room.send_packet_to_users(packet)
        return CommandResponse.OK, ""

    def remove_user_trace(self, user: User):
        room = self.__room_handler.get_room_from_user(user)
        if room is not None:
            self.__room_handler.remove_user_from_room(user, room)

    def interpret_command(self, user: User, packet: Packet):
        if packet.command_nb in Commands:
            response, info = self.__command_list[packet.command_nb](user, packet.param)
            if response == CommandResponse.PARAM_ERROR:
                user.add_to_output_queue(Packet(Commands.ERROR, info))
