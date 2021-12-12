from .Session import Session
from common.utils.password import validate_password


class Room:
    def __init__(self, name: str, password: str):
        self.__name = name
        self.__password = password
        self.__users = []

    def __str__(self):
        return self.__name

    def add_user(self, user: Session, password : str):
        if not validate_password(self.__password, password):
            return
        self.__users.append(user)

    def remove_user(self, user: Session):
        self.__users.remove(user)

    def send_packet_to_users(self, message):
        for user in self.__users:
            user.queue_to_send(message)

    def has_user(self, user: Session):
        return user in self.__users
