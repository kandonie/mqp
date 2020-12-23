from enum import Enum


class PWMVals(Enum):
    ## CW/CCW refers to motor rotation
    FULL_CW = "2000"
    FULL_CCW = "1000"
    STOPPED = "1500"
