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

    def remove_user(self, user: User):
        self.__users.remove(user)

    def send_packet_to_users(self, message):
        for user in self.__users:
            user.add_to_output_queue(message)

    def has_user(self, user: User):
        return user in self.__users
