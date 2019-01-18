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

    def remove_user_from_room(self, user: User, room: Room):
        if room in self.__rooms and room.has_user(user):
            room.remove_user(user)

    def is_user_in_room(self, user: User) -> bool:
        for room in self.__rooms:
            if room.has_user(user):
                return True
        return False

    def get_room_from_user(self, user: User) -> Room or None:
        for room in self.__rooms.values():
            if room.has_user(user):
                return room
        return None
