from src.Guidance.GuidanceEnums import BehavioralStates_T
import time

class ESTOP():

    def __init__(self, drive, weapon):
        """
        intialize the ESTOP State
        :param drive: [Drive] the drive instance
        :param weapon: [Weapon] the weapon instance
        """
        self.drive = drive
        self.weapon = weapon

    def execute(self, robot_data, state_args):
        """
        repeatedly sends STOP to the drive and weapon, should be as short as possible
        :param robot_data: the robot data (sensor info, CV, so on)
        :param state_args: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        self.drive.stop()
        self.weapon.stop()
        time.sleep(1)


    def getType(self):
        """
        :return: the behavior state
        """
        return BehavioralStates_T.ESTOP

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs)
        """
        return None
