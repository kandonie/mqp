from enum import Enum

class ButtonStrings(Enum):
    ESTOP = "ESTOP"
    RC = "RC"
    WEAPON_INIT = "Weapon Init"
    DRIVE_INIT = "Drive Init"
    GAME_OVER = "Game Over"

    #Testing after this
    CW_SQUARE = "Clockwise Square"
    CCW_SQUARE = "Counter Clockwise Square"
    CW_TURN = "Clockwise Turn (full circle)"
    CCW_TURN = "Counter Clockwise Turn (full circle)"