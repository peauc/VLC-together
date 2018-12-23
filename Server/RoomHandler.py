import logging
from .User import User
from .Room import Room


class RoomHandler:
    def __init__(self):
        self.__rooms = {}

    def add_user_to_room(self, user: User, room_name: str, password=""):
            if room_name not in self.__rooms:
                logging.debug(f"Added user {user.sock.getpeername()} to room {room_name}")
                self.__rooms[room_name] = Room(room_name, password)
            self.__rooms[room_name].add_user(user, password)

