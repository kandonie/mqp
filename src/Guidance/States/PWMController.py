from src.Guidance.GuidanceEnums import BehavioralStates_T
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars_T
from src.Robot_Locomotion.MotorEnums import PWMVals_T


class PWMController:

    def __init__(self, drive):
        """
        Initialize the state
        :param drive: the drive
        :param weapon: the weapon
        """
        self.drive = drive
        self.has_sent = False
        # remember prev vals, so we only send if pwm changed
        self.motor_vals = {SetJSONVars_T.MOTOR1_PWM: PWMVals_T.STOPPED, SetJSONVars_T.MOTOR2_PWM: PWMVals_T.STOPPED,
                           SetJSONVars_T.WEAPON_PWM: PWMVals_T.STOPPED, }

    def execute(self, robot_data, state_args):
        """
        sends a PWM signal from the GUI to the motors
        :param robot_data: the robot data (sensor info, CV, so on)
        :param state_args: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        motor = state_args[0]
        pwm = state_args[1]
        if not self.has_sent or not self.motor_vals[motor] == pwm:
            self.motor_vals[motor] = pwm
            self.drive.setPWM(motor.value, pwm)
            self.has_sent = True
        return False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates_T.PWM

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
        """
        return None
