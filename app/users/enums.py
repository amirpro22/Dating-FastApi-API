


from enum import Enum


class Action(Enum):
    like = "like"
    dislike = "dislike"
    processing = "processing"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Action))