from Guidance.GuidanceEnums import BehavioralStates, RobotDataTopics
import time
class PolygonalMovement():
    def __init__(self, drive):
        """
        describe state here
        :param drive:
        :param weapon:
        """
        self.drive = drive
        self.resetVars()

    def execute(self, robotData):
        numSides = robotData[RobotDataTopics.BEHAVIOR_SPECIFIC_DATA][1]
        if numSides != self.goalSides:
            self.resetVars()
            self.goalSides = numSides
            self.angle = (numSides - 2) * 180 / numSides
        elif self.done:
            return

        if self.isTurning:
            self.drive.turn(self.angle)
            self.isTurning = False
        else:
            self.drive.driveDistance(1)  # drive one meter
            self.sidesCompleted += 1
            self.isTurning = True

        if self.sidesCompleted == self.goalSides:
            self.drive.stop()
            nSides = self.sidesCompleted
            self.resetVars()
            self.done = True
            self.goalSides = nSides #to make the first if false

    def resetVars(self):
        self.sidesCompleted = 0
        self.goalSides = 0
        self.angle = 0
        self.isTurning = False
        self.done = False


    def getType(self):
        return BehavioralStates.MOVEMENT_TEST