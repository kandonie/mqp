from src.Guidance.GuidanceEnums import BehavioralStates
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars
from src.Robot_Locomotion.MotorEnums import PIDVals


class PIDTuner():

    def __init__(self, wifi):
        """
        Initialize the state
        """
        self.hasSent = False
        self.wifi = wifi
        self.pidVals = {SetJSONVars.KP: PIDVals.KP_DEFAULT, SetJSONVars.KI: PIDVals.KI_DEFAULT,
                        SetJSONVars.KD: PIDVals.KD_DEFAULT, }
        self.target = None

    def execute(self, robotData, stateArgs):
        """
        sends PID gain values from the GUI to the robot
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """
        gain = stateArgs[0]
        gain_val = stateArgs[1]
        target = stateArgs[2]
        tuning_gain = "tuning_" + gain.value
        if not self.hasSent or not self.pidVals[gain] == gain_val or not self.target == target :
            self.pidVals[gain] = gain_val
            self.wifi.sendInfo({tuning_gain: 1,
                                gain.value: gain_val,
                                SetJSONVars.PID_TARGET.value: target})
            self.hasSent = True
            self.wifi.sendInfo({tuning_gain: 0})
            self.target = target
            # return True
        return False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates.PID

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
        """
        return None
