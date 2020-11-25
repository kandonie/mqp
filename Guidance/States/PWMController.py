from Guidance.GuidanceEnums import BehavioralStates, RobotDataTopics

class PWMController():


    def __init__(self, drive):
        """
        describe state here
        :param drive:
        :param weapon:
        """
        self.drive = drive
        self.hasSent = False
        self.pwm = "0"

    def execute(self, robotData):
        pwm = robotData[RobotDataTopics.BEHAVIOR_SPECIFIC_DATA][1]
        if not self.hasSent or not self.pwm is pwm:
            self.pwm = pwm
            self.drive.drive(pwm)
            self.hasSent = True


    def getType(self):
        return BehavioralStates.PWM