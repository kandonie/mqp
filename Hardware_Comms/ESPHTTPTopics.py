from enum import Enum


class HTTPTopics(Enum):
    """
    topic used for wifi comms
    """
    MAIN = "/generaltest"


class RobotMovementType(Enum):
    """
    the type of movement control for the drive
    """
    PWM_CONTROLLED = "rcMode"
    DRIVE_DISTANCE = "distanceMode"
    TURN_ANGLE = "gyroMode"


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
    DESIRED_DISTANCE = 'desiredDist'
    MOVEMENT_TYPE = "RobotMovementType"
    WEAPON_ENABLE_CHANGE = 'Weapon Enabled Changed State'
    DRIVE_ENABLE_CHANGE = "Drive Enabled Changed State"


class GetJSONVars(Enum):
    """
    The json variables the can be acquired through wifi
    aka info received from the robot about the robot
    """
    HEADING = 'getHeading'
    DRIVE_CURRENT = 'getDriveCurrent'
    WEAPON_CURRENT = 'getWeaponCurrent'
    IS_UPSIDE_DOWN = 'getOrientation'
    WIFI_STRENGTH = 'getSignalStrength'
