from enum import Enum


class AndromedaCollections(Enum):
    STARGAZE_PUNK = (0,)
    ANDROMA_PUNK = (1,)
    ANDROMAVERSE = 3

    @classmethod
    def from_str(cls, str):
        s = str.lower()
        if s in ["stargaze_punk", "stargaze punk", "stargaze-punk", "spunk", "sc"]:
            return cls.STARGAZE_PUNK
        if s in ["androma_punk", "androma punk", "androma-punk", "apunk"]:
            return cls.ANDROMA_PUNK
        if s in ["andromaverse", "egg"]:
            return cls.ANDROMAVERSE
