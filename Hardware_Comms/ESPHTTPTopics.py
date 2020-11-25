from enum import Enum

class HTTPTopics(Enum):
    """ topic used for wifi comms"""
    MAIN = "/generaltest"

class SetJSONVars(Enum):
    """The json variables that can be set through wifi"""
    MOTOR1_PWM = 'motor1pwm'
    MOTOR2_PWM = 'motor2pwm'
    WEAPON_PWM = 'weaponMode'
    DESIRED_HEADING = 'desiredHeading'

class GetJSONVars(Enum):
    """The json variables the can be acquired through wifi"""
    HEADING = 'getHeading'
    DRIVE_CURRENT = 'getDriveCurrent'
    WEAPON_CURRENT = 'getWeaponCurrent'
    IS_UPSIDE_DOWN = 'getOrientation'
    WIFI_STRENGTH = 'getSignalStrength'
