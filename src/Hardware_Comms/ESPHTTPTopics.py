from enum import Enum


class HTTPTopics(Enum):
    """
    topic used for wifi comms
    """
    MAIN = "/generaltest"
    ROBOT_DATA = "/getRobotData"
    ESTOP = "/ESTOP"


class RobotMovementType(Enum):
    """
    the type of movement control for the drive
    """
    PWM_CONTROLLED = "rcMode"
    DRIVE_DISTANCE = "distanceMode"
    TURN_ANGLE = "gyroMode"
    DISABLE_ROBOT = "disabled"
    CONFIGURE = "configure"

    @classmethod
    def list_states(cls):
        role_names = [member.value for role, member in cls.__members__.items()]
        return role_names

class SetJSONVars(Enum):
    """
    The json variables that can be set through wifi
    AKA things to set on the robot
    """
    MOTOR1_PWM = 'motor1pwm'
    MOTOR2_PWM = 'motor2pwm'
    WEAPON_PWM = 'weapon_pwm'
    CURRENT_HEADING = 'currentHeading'
    DESIRED_HEADING = 'desiredHeading'
    SETTING_HEADING = "setting_heading"
    DESIRED_DISTANCE = 'desiredDistance'
    SETTING_DISTANCE = "setting_distance"
    MOVEMENT_TYPE = "RobotMovementType"
    WEAPON_ENABLE_CHANGE = 'WeaponArmedState'
    DRIVE_ENABLE_CHANGE = "ArmDriveState"
    TUNING_KP = "tuning_kp"
    TUNING_KI = "tuning_ki"
    TUNING_KD = "tuning_kd"
    KP = "kp"
    KI = "ki"
    KD = "kd"


class GetJSONVars(Enum):
    """
    The json variables the can be acquired through wifi
    aka info received from the robot about the robot
    """
    HEADING = 'getHeading'
    DRIVE_CURRENT = 'getDriveCurrent'
    WEAPON_CURRENT = 'getWeaponCurrent'
    # IS_UPSIDE_DOWN = 'getOrientation'
    # WIFI_STRENGTH = 'getSignalStrength'