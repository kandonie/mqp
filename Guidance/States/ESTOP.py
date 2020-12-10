from Guidance.GuidanceEnums import BehavioralStates

class ESTOP():


    def __init__(self, drive, weapon):
        """
        describe state here
        :param drive:
        :param weapon:
        """
        self.drive = drive
        self.weapon = weapon

    def execute(self, robotData, stateArgs):
        self.drive.stop()
        self.weapon.stop()
        self.sent = True

    def getType(self):
        return BehavioralStates.ESTOP
