from enum import Enum, IntEnum


class PriceUSD(Enum):
    NO_LIMIT = 1
    UNDER_25 = 2
    UNDER_10 = 3
    UNDER_5 = 4
    UNDER_1 = 5


class PriceTIX(Enum):
    NO_LIMIT = 1
    UNDER_25 = 2
    UNDER_10 = 3
    UNDER_5 = 4
    UNDER_1 = 5


class Popularity(Enum):
    NONE = 1
    BAD = 2
    DECENT = 3
    GOOD = 4


class CMC(IntEnum):
    NONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6