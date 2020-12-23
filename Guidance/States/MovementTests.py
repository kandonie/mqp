from Guidance.GuidanceEnums import BehavioralStates


class PolygonalMovement():
    def __init__(self, drive):
        """
        initializes the state
        :param drive: the drive
        :param weapon: the weapon
        """
        self.drive = drive
        self.resetVars()

    def execute(self, robotData, stateArgs):
        """
        drives in a polygon with stateArgs number of sides
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        numSides = stateArgs
        if numSides != self.goalSides:
            self.resetVars()
            self.goalSides = numSides
            self.angle = (numSides - 2) * 180 / numSides
        elif self.done:
            return True

        if self.isTurning:
            self.drive.turnAngle(self.angle)
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
            self.goalSides = nSides  # to make the first if false
            return True

        return False

    def resetVars(self):
        """
        resets all of the variables to a default state
        """
        self.sidesCompleted = 0
        self.goalSides = 0
        self.angle = 0
        self.isTurning = False
        self.done = False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates.MOVEMENT_TEST

    def getNextState(self):
        """
       Returns the state to transition to after this one
       :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
       """
        return (BehavioralStates.STOP, None)
