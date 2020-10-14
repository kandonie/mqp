from enum import Enum

class States(Enum):
    IDLE = 0
    REMOTE_CONTROL = 1
    AUTONOMOUS_STARTUP = 3
    ATTACKING = 4
    PINNING = 5
    STATIONARY_OPPONENT = 6
    WEAPON_STALL = 7
    MATCH_OVER = 8
