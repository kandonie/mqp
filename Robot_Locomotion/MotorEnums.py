from enum import Enum


class PWMVals(Enum):
    FULL_CW = "2000"
    FULL_CCW = "1000"
    STOPPED = "1660"


    # values from 1000 - 2000
    # with 1660 being stopped