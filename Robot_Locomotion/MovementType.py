from enum import Enum

class MovementType(Enum):
    TURN = "Turn (degrees)"
    DRIVE_STRAIGHT = "Drive Straight (meters)"
    SQUARE = "Square (side len)"
    STOP = "Stop (input irrelevant)"