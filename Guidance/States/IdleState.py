
from Guidance.states import States

class IdleState():


    def __init__(self, drive, weapon):
        """
        describe state here
        :param drive:
        :param weapon:
        """
        self.drive = drive
        self.weapon = weapon

    def execute(self, robotData):
        pass

    def getType(self):
        return States.ESTOP