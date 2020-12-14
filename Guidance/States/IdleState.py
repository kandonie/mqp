from Guidance.GuidanceEnums import BehavioralStates


class IdleState():

    def __init__(self, drive, weapon):
        """
        describe state here
        :param drive:
        :param weapon:
        """
        self.drive = drive
        self.weapon = weapon
        # TODO remove
        self.sent = False

    def execute(self, robotData, stateArgs):
        if not self.sent:
            self.drive.stop()
            self.weapon.stop()
            self.sent = True
        return False

    def getType(self):
        return BehavioralStates.STOP

    def getNextState(self):
        return None
