from enum import Enum

class IntelligenceStates(Enum):
    IDLE = "Idle"
    RC = "Remote Control"
    AUTO = "Autonomous"

class States(Enum):
    ESTOP = "ESTOP"
    MATCH_START = "match start"
    UPSIDE_DOWN_DISAGREEMENT = "upside down disagreement"
    UPSIDE_DOWN = "upside down"
    ROBOT_INVISIBLE = "CAN'T SEE ROBOT :("
    BACK_OFF = "backing off"