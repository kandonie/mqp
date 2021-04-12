from enum import Enum

class CVTopics(Enum):
    HEADING = "CV robot heading"
    POSITION = "CV robot position" # value will be tuple of (x, y)
    OPPONENT_HEADING = "Opponent heading"
    OPPONENT_POSITION = "Opponent position" # value will be tuple of (x, y)
    TARGET_HEADING = "CV target heading"
    TARGET_DISTANCE = "CV target distance"