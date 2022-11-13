from enum import Enum

class ResponseErrors(Enum):
    generic_error: str = 'not_found'

    @classmethod
    def is_error(cls, value):
        return value in cls._value2member_map_ 