from enum import Enum

class IntelligenceStates(Enum):
    """The states of autonomy of the robot
    """
    IDLE = "Idle"
    RC = "Remote Control"
    AUTO = "Autonomous"

class StateDataTopics(Enum):
    INTELLIGENCE_STATE = "Intelligence State Data Topic"
    MOVEMENT = "GUI Movement Data Topic"

class States(Enum):
    """the autonomous states of the robot
    """
    ESTOP = "ESTOP"
    MATCH_START = "match start"
    UPSIDE_DOWN_DISAGREEMENT = "upside down disagreement"
    UPSIDE_DOWN = "upside down"
    ROBOT_INVISIBLE = "CAN'T SEE ROBOT :("
    BACK_OFF = "backing off"