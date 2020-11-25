from enum import Enum


class PWMVals(Enum):
    FULL_CW = "100"
    FULL_CCW = "-100"
    STOPPED = "0"