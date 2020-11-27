from enum import Enum

class RobotDataTopics(Enum):
    BEHAVIORAL_ARGS = "behavior specific data"
    BEHAVIORAL_STATE = "current behavior"

class IntelligenceStates(Enum):
    """The states of autonomy of the robot
    """
    IDLE = "Idle"
    RC = "Remote Control"
    AUTO = "Autonomous"

class BehavioralStates(Enum):
    """the autonomous states of the robot
    # """
    ESTOP = "ESTOP"
    MOVEMENT_TEST = "Movement tests"
    PWM = "PWM controller"
    # MATCH_START = "match start"
    # UPSIDE_DOWN_DISAGREEMENT = "upside down disagreement"
    # UPSIDE_DOWN = "upside down"
    # ROBOT_INVISIBLE = "CAN'T SEE ROBOT :("
    # BACK_OFF = "backing off"