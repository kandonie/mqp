from src.Guidance.GuidanceEnums import BehavioralStates
from src.Robot_Locomotion.MotorEnums import PWMVals


class Attack():

    def __init__(self, drive, weapon):
        """
        initialize the state
        """
        # This function can have whatever params you want. usually weapon, drive, and wifi
        self.drive = drive
        self.weapon = weapon
        pass

    def execute(self, robotData, stateArgs):
        """
        move toward opponent position to attack
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        self.drive.driveToOpponent()
        # return True

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates.ATTACK

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
        """
        return (BehavioralStates.STOP, None)
