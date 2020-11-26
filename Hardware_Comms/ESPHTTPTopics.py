from enum import Enum

class HTTPTopics(Enum):
    """ topic used for wifi comms"""
    MAIN = "/generaltest"

class SetJSONVars(Enum):
    """The json variables that can be set through wifi"""
    MOTOR1_PWM = 'motor1pwm'
    MOTOR2_PWM = 'motor2pwm'
    WEAPON_PWM = 'weapon_pwm'
    CURRENT_HEADING = 'currentHeading'
    # These two should always be sent togther
    # robot turn heading first then moves set distance
    DESIRED_HEADING = 'desiredHeading'
    DISTANCE = 'movmentDistance'
    ARM_DISARM_SYSTEMS =  'arm/disarm sytems'

class ARM(Enum):
    #signals go through, robot just doesnt respond
    ARM_ALL = 'Weapon AND Drive Armed'
    ARM_DRIVE = 'Drive ONLY Armed'
    ARM_WEAPON = 'Weapon ONLY Armed'
    DISARM_ALL = 'Totally Disarmed'


class GetJSONVars(Enum):
    """The json variables the can be acquired through wifi"""
    HEADING = 'getHeading'
    DRIVE_CURRENT = 'getDriveCurrent'
    WEAPON_CURRENT = 'getWeaponCurrent'
    IS_UPSIDE_DOWN = 'getOrientation'
    WIFI_STRENGTH = 'getSignalStrength'
