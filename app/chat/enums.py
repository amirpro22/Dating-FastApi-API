
from enum import Enum


class ActionType(Enum):
    message = "message"
    typing = "typing"


    @staticmethod
    def list():
        return list(map(lambda c: c.value, ActionType))