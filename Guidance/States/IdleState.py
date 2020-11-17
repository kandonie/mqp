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
        #TODO remove
        self.sent = False

    def execute(self, robotData):
        if not self.sent:
            self.drive.stop()
            self.weapon.stop()
            self.sent = True

    def getType(self):
        return BehavioralStates.ESTOP