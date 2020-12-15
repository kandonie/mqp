from enum import Enum


class IntelligenceStates(Enum):
    """
    The states of autonomy of the robot
    """
    IDLE = "Idle"
    RC = "Remote Control"
    AUTO = "Autonomous"


class BehavioralStates(Enum):
    """
    the behavioral states of the robot
    """
    ESTOP = "ESTOP State"
    STOP = "Stopped State"
    RC = "RC State"
    MOVEMENT_TEST = "Polygonal Movement State"
    PWM = "PWM Controlling State"