from Guidance.GuidanceEnums import BehavioralStates


class Stop():

    def __init__(self, drive, weapon):
        """
        sends stop once then does nothing
        :param drive: the drive
        :param weapon: the weapon
        """
        self.drive = drive
        self.weapon = weapon
        self.sent = False

    def execute(self, robotData, stateArgs):
        """
        Sends stop once then does nothing and always returns false
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        if not self.sent:
            self.drive.stop()
            self.weapon.stop()
            self.sent = True
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
        return None
