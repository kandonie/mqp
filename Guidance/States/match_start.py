from Guidance.GuidanceEnums import BehavioralStates


class MatchStart():

    def __init__(self):
        """
        initialize the state
        """
        # This function can have whatever params you want.
        pass

    def execute(self, robotData, stateArgs):
        """
        repeatedly sends STOP to the drive and weapon, should be as short as possible
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        return False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates.STOP

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
        """
        return (BehavioralStates.STOP, None)
