from Guidance.GuidanceEnums import BehavioralStates, RobotDataTopics

class PWMController():


    def __init__(self, drive):
        """
        describe state here
        :param drive:
        :param weapon:
        """
        self.drive = drive

    def execute(self, robotData):
        pwm = robotData[RobotDataTopics.BEHAVIOR_SPECIFIC_DATA][1]
        self.drive.drive(pwm)


    def getType(self):
        return BehavioralStates.PWM