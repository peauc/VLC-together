from .User import User
from Common.Utils.password import validate_password


class Room:
    def __init__(self, name: str, password: str):
        self.__name = name
        self.__password = password
        self.__users = []

    def add_user(self, user: User, password : str):
        if not validate_password(self.__password, password):
            return
        self.__users.append(user)
        self.__send_message_to_every_users(f"{user.sock.getpeername()} joined the room")

    def __send_message_to_every_users(self, param):
        for user in self.__users:
            user.add_to_output_queue(param)
