from src.Guidance.GuidanceEnums import BehavioralStates
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, RobotMovementType
from src.Robot_Locomotion.MotorEnums import MovementVals


class SetHeading():

    def __init__(self, wifi):
        """
        Initialize the state
        """
        self.hasSent = False
        self.wifi = wifi
        self.headingVal = {SetJSONVars.DESIRED_HEADING: MovementVals.HEADING_DEFAULT}

    def execute(self, robotData, stateArgs):
        """
        sends desired heading value from the GUI to the robot
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        heading = stateArgs[0]
        heading_val = stateArgs[1]
        if not self.hasSent or not self.headingVal[heading] == heading_val:
            self.headingVal[heading] = heading_val
            self.wifi.sendInfo(SetJSONVars.SETTING_HEADING.value, 1)
            self.wifi.sendInfo(heading.value, heading_val)
            self.hasSent = True
            self.wifi.sendInfo(SetJSONVars.SETTING_HEADING.value, 0)
            self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.TURN_ANGLE.value)
        return False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates.SET_HEADING

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
        """
        return None
