from enum import Enum


class AndromedaCollections(Enum):
    STARGAZE_PUNKS = (0,)
    ANDROMA_PUNKS = (1,)
    ANDROMAVERSE = 3

    @classmethod
    def from_str(cls, str):
        s = str.lower()
        if s in ["stargaze_punk", "stargaze punk", "stargaze-punk", "spunk", "sc"]:
            return cls.STARGAZE_PUNKS
        if s in ["androma_punk", "androma punk", "androma-punk", "apunk"]:
            return cls.ANDROMA_PUNKS
        if s in ["andromaverse", "egg"]:
            return cls.ANDROMAVERSE
