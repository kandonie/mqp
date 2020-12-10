from enum import Enum

#this might end up including GETJSONVARs and CV or something like that
#TODO use or delete
class RobotDataTopics(Enum):
    PLACEHOLDER = "Placeholder"

class IntelligenceStates(Enum):
    """The states of autonomy of the robot
    """
    IDLE = "Idle"
    RC = "Remote Control"
    AUTO = "Autonomous"

class BehavioralStates(Enum):
    """the autonomous states of the robot
    # """
    ESTOP = "ESTOP State"
    STOP = "Stopped State"
    RC = "RC State"
    MOVEMENT_TEST = "Polygonal Movement State"
    PWM = "PWM Controlling State"
    # MATCH_START = "match start"
    # UPSIDE_DOWN_DISAGREEMENT = "upside down disagreement"
    # UPSIDE_DOWN = "upside down"
    # ROBOT_INVISIBLE = "CAN'T SEE ROBOT :("
    # BACK_OFF = "backing off"
