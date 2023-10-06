


from enum import Enum


class Gender(Enum):
    male = "male"
    female = "female"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Gender))