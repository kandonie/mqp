from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, RobotMovementType
from src.Guidance.GuidanceEnums import BehavioralStates


class Robot:
    """
    the computer representation of the drive
    """

    def __init__(self, wifi, drive, weapon):
        """
        initializes drive
        :param wifi:  the wifi
        """
        self.wifi = wifi
        self.drive = drive
        self.weapon = weapon

    def disable(self):
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.DISABLE_ROBOT.value)

    def estop(self):
        self.wifi.sendInfo(BehavioralStates.ESTOP.value, "ESTOP")
