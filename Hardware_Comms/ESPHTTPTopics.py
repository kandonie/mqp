from enum import Enum

class HTTPTopics(Enum):
    MAIN = "/general"

class StateMachineTopics(Enum):
    SET_PWM = "set pwm"
    SET_HEADING = "set heading"
    ESTOP = "ESTOP"
    INTELLIGENCE_STATE = "intelligence state"

class SetJSONVars(Enum):
    MOTOR1_PWM = 'motor1pwm'
    MOTOR2_PWM = 'motor2pwm'
    WEAPON_PWM = 'weaponMode'
    DESIRED_HEADING = 'desiredHeading'

class GetJSONVars(Enum):
    HEADING = 'getHeading'
    DRIVE_CURRENT = 'getDriveCurrent'
    WEAPON_CURRENT = 'getWeaponCurrent'
    IS_UPSIDE_DOWN = 'getOrientation'
    WIFI_STRENGTH = 'getSignalStrength'
