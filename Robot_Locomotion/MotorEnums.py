from enum import Enum


class PWMVals(Enum):
    ## CW/CCW refers to motor rotation
    FULL_CW = "1700"
    FULL_CCW = "1300"
    STOPPED = "1500"

    # values from 1000 - 2000
    # with 1660 being stopped
