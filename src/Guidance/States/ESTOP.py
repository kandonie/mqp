from src.Guidance.GuidanceEnums import BehavioralStates
import time
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, RobotMovementType


class ESTOP():

    def __init__(self, robot):
        """
        intialize the ESTOP State
        :param drive: [Drive] the drive instance
        :param weapon: [Weapon] the weapon instance
        """
        self.robot = robot

    def execute(self, robotData, stateArgs):
        """
        repeatedly sends STOP to the drive and weapon, should be as short as possible
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        self.robot.estop()
        self.robot.disable()
        time.sleep(1)
        return False


    def getType(self):
        """
        :return: the behavior state
        """
        return BehavioralStates.ESTOP

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs)
        """
        return None
