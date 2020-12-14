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

    def execute(self, robotData, stateArgs):
        motor = stateArgs[0]
        pwm = stateArgs[1]
        if not self.hasSent or not self.motorVals[motor] == pwm:
            self.motorVals[motor] = pwm
            self.drive.setPWM(motor.value, pwm)
            self.hasSent = True
        return False

    def getType(self):
        return BehavioralStates.PWM

    def getNextState(self):
        return None
