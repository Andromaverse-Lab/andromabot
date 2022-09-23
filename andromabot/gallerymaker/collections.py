from enum import Enum


class AndromedaCollections(Enum):
    UNKNOWN = 0
    STARGAZE_PUNKS = 1
    ANDROMA_PUNKS = 2
    ANDROMAVERSE = 3
    FORGOTTEN = 4

    @classmethod
    def from_str(cls, str):
        s = str.lower()
        if s in ["stargaze_punk", "stargaze punk", "stargaze-punk", "spunk", "sc"]:
            return cls.STARGAZE_PUNKS
        if s in ["androma_punk", "androma punk", "androma-punk", "apunk"]:
            return cls.ANDROMA_PUNKS
        if s in ["andromaverse", "egg"]:
            return cls.ANDROMAVERSE
        if s in ["forgotten", "funk", "fpunk", "fp"]:
            return cls.FORGOTTEN
        return cls.UNKNOWN
