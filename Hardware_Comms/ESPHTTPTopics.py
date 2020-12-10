from enum import Enum

class HTTPTopics(Enum):
    """ topic used for wifi comms"""
    MAIN = "/generaltest"

class RobotMovementType(Enum):
    PWM_CONTROLLED = "rcMode"
    DRIVE_DISTANCE = "distanceMode"
    TURN_ANGLE = "gyroMode"

class SetJSONVars(Enum):
    """The json variables that can be set through wifi"""
    MOTOR1_PWM = 'motor1pwm'
    MOTOR2_PWM = 'motor2pwm'
    WEAPON_PWM = 'weapon_pwm'
    CURRENT_HEADING = 'currentHeading'
    # These two should always be sent togther
    # robot turn heading first then moves set distance
    DESIRED_HEADING = 'desiredHeading'
    DESIRED_DISTANCE = 'desiredDist'
    MOVEMENT_TYPE = "RobotMovementType"
    ARM_WEAPON =  'Weapon Armed State'
    ARM_DRIVE = "Arm Drive State"

class GetJSONVars(Enum):
    """The json variables the can be acquired through wifi"""
    HEADING = 'getHeading'
    DRIVE_CURRENT = 'getDriveCurrent'
    WEAPON_CURRENT = 'getWeaponCurrent'
    IS_UPSIDE_DOWN = 'getOrientation'
    WIFI_STRENGTH = 'getSignalStrength'
