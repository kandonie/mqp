from src.Guidance.GuidanceEnums import BehavioralStates_T


class PolygonalMovement():
    def __init__(self, drive):
        """
        initializes the state
        :param drive: the drive
        :param weapon: the weapon
        """
        self.drive = drive
        self.resetVars()

    def execute(self, robot_data, state_args):
        """
        drives in a polygon with stateArgs number of sides
        :param robot_data: the robot data (sensor info, CV, so on)
        :param state_args: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        num_sides = state_args
        if num_sides != self.goal_sides:
            self.resetVars()
            self.goal_sides = num_sides
            self.angle = (num_sides - 2) * 180 / num_sides
        elif self.done:
            return True

        if self.is_turning:
            self.drive.turnAngle(self.angle)
            self.is_turning = False
        else:
            self.drive.driveDistance(1)  # drive one meter
            self.sides_completed += 1
            self.is_turning = True

        if self.sides_completed == self.goal_sides:
            self.drive.stop()
            nSides = self.sides_completed
            self.resetVars()
            self.done = True
            self.goal_sides = nSides  # to make the first if false
            return True

        return False

    def resetVars(self):
        """
        resets all of the variables to a default state
        """
        self.sides_completed = 0
        self.goal_sides = 0
        self.angle = 0
        self.is_turning = False
        self.done = False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates_T.MOVEMENT_TEST

    def getNextState(self):
        """
       Returns the state to transition to after this one
       :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
       """
        return (BehavioralStates_T.STOP, None)
