from enum import Enum


class IntelligenceStates(Enum):
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


class BehavioralStates(Enum):
    """
    the behavioral states of the robot
    """
    ESTOP = "ESTOP State"
    STOP = "Stopped State"
    RC = "RC State"
    MOVEMENT_TEST = "Polygonal Movement State"
    SET_HEADING = "Set Heading State"
    SET_DISTANCE = "Set Distance State"
    PWM = "PWM Controlling State"
    PID = "PID Tuning State"
    MATCH_START = "Match Start State"
    END_MATCH = "Match End State"
    ATTACK = "Attack State"