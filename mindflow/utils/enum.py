from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))
