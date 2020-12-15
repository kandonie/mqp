from Guidance.GuidanceEnums import BehavioralStates
from Hardware_Comms.ESPHTTPTopics import SetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals


class PWMController():

    def __init__(self, drive):
        """
        Initialize the state
        :param drive: the drive
        :param weapon: the weapon
        """
        self.drive = drive
        self.hasSent = False
        # remember prev vals, so we only send if pwm changed
        self.motorVals = {SetJSONVars.MOTOR1_PWM: PWMVals.STOPPED, SetJSONVars.MOTOR2_PWM: PWMVals.STOPPED,
                          SetJSONVars.WEAPON_PWM: PWMVals.STOPPED, }

    def execute(self, robotData, stateArgs):
        """
        sends a PWM signal from the GUI to the motors
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        motor = stateArgs[0]
        pwm = stateArgs[1]
        if not self.hasSent or not self.motorVals[motor] == pwm:
            self.motorVals[motor] = pwm
            self.drive.setPWM(motor.value, pwm)
            self.hasSent = True
        return False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates.PWM

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
        """
        return None
