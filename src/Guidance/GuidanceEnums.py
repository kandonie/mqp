from enum import Enum


class IntelligenceStates_T(Enum):
    """
    The states of autonomy of the robot
    """
    IDLE = "Idle"
    RC = "Remote Control"
    AUTO = "Autonomous"

    @classmethod
    def list_states(cls):
        role_names = [member.value for role, member in cls.__members__.items()]
        return role_names


class BehavioralStates_T(Enum):
    """
    the behavioral states of the robot
    """
    ESTOP = "ESTOP State"
    STOP = "Stopped State"
    RC = "RC State"
    MOVEMENT_TEST = "Polygonal Movement State"
    PWM = "PWM Controlling State"
    MATCH_START = "Match Start State"
    END_MATCH = "Match End State"