from Guidance.GuidanceEnums import BehavioralStates, RobotDataTopics
from Hardware_Comms.ESPHTTPTopics import SetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals

class PWMController():


    def __init__(self, drive):
        """
        describe state here
        :param drive:
        :param weapon:
        """
        self.drive = drive
        self.hasSent = False
        self.motorVals = {SetJSONVars.MOTOR1_PWM:PWMVals.STOPPED,  SetJSONVars.MOTOR2_PWM:PWMVals.STOPPED, SetJSONVars.WEAPON_PWM:PWMVals.STOPPED, }

    def execute(self, robotData):
        args = robotData[RobotDataTopics.BEHAVIOR_SPECIFIC_DATA][1]
        motor = args[0]
        pwm = args[1]
        if not self.hasSent or not self.motorVals[motor] == pwm:
            self.motorVals[motor] = pwm
            self.drive.setPWM(motor.value, pwm)
            self.hasSent = True

    def getType(self):
        return BehavioralStates.PWM