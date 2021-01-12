from src.Robot_Locomotion.drive import Drive
from src.Robot_Locomotion.weapon import Weapon
from src.Guidance.GuidanceEnums import BehavioralStates_T, IntelligenceStates_T
from src.Guidance.States.stop import Stop
from src.Guidance.States.PolygonalMovement import PolygonalMovement
from src.Guidance.States.PWMController import PWMController
from src.Guidance.States.RemoteControl import RemoteControl
from src.Guidance.States.match_start import MatchStart
from src.Guidance.States.EndMatch import MatchEnd
from src.Guidance.States.ESTOP import ESTOP
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars_T, GetJSONVars_T
import threading
from src.Sensing.RobotDataManager import RobotDataManager


class StateMachine:
    """controls the decisions of the robot.
    """

    def __init__(self, wifi):
        """
        initializes the state machine
        :param wifi: [WiFiComms] The wifi object used to communicate with the robot
        """

        # init vars
        self.wifi = wifi
        # set initial enabled state to disabled
        # TODO maybe put this somewhere else
        self.wifi.sendInfo(SetJSONVars_T.WEAPON_ENABLE_CHANGE.value, "false")
        self.wifi.sendInfo(SetJSONVars_T.DRIVE_ENABLE_CHANGE.value, "false")
        self.drive = Drive(wifi)
        self.weapon = Weapon(wifi)
        self.state = self.makeState(BehavioralStates_T.STOP)
        self.state_args = None
        self.intelligence_state = IntelligenceStates_T.IDLE
        # robotData is a dict with Behavioral_Args and Behavioral_State
        self.robot_data_manager = RobotDataManager.getInstance()
        self.robot_data_manager.attachObserver(self)
        # locks for accessing state
        self.robot_state_lock = threading.Lock()

    def runStateMachine(self):
        """
        executes states based on current state
        """
        while True:
            # get a copy of the current robot data
            data = self.robot_data_manager.getRobotData()

            # execute state with that data
            self.robot_state_lock.acquire()
            done_state = self.state.execute(data, self.state_args)
            self.robot_state_lock.release()

            # when we are ready to go to the next state
            if done_state:
                new_state_with_args = self.state.getNextState()
                # none is a default option
                if new_state_with_args == None:
                    new_state_with_args = (BehavioralStates_T.STOP, None)
                self.determineNextState(new_state_with_args)

    def makeState(self, state):
        """
        makes an instance of the next state
        :param state: the next state
        :return: the new state
        """
        if state == BehavioralStates_T.STOP:
            state = Stop(self.drive, self.weapon)
        elif state == BehavioralStates_T.MOVEMENT_TEST:
            state = PolygonalMovement(self.drive)
        elif state == BehavioralStates_T.PWM:
            state = PWMController(self.drive)
        elif state == BehavioralStates_T.RC:
            state = RemoteControl(self.drive, self.weapon)
        elif state == BehavioralStates_T.ESTOP:
            state = ESTOP(self.drive, self.weapon)
        elif state == BehavioralStates_T.MATCH_START:
            state = MatchStart()
        elif state == BehavioralStates_T.END_MATCH:
            state = MatchEnd()
        return state

    def determineNextState(self, args):
        """
        determines the next state of the robot and sets appropriate vars
        :param args: the arguments as None or (state, stateArgs)
        """
        # Check for correct input, if it's none that means we don't want a new state
        if args is not None and len(args) == 2:
            # if we are in IDLE, do nothing. But bypass this for ESTOP
            if self.intelligence_state == IntelligenceStates_T.IDLE and args[0] != BehavioralStates_T.ESTOP:
                # if we aren't in stop state, change to stop state, otherwise do nothing in IDLE
                if self.state.getType() != BehavioralStates_T.STOP:
                    self.robot_state_lock.acquire()
                    self.switchState(BehavioralStates_T.STOP)
                    self.robot_state_lock.release()
                print("psst  .... we are in IDLE. Change to auto to send robot messages")
            else:
                # change the state
                self.robot_state_lock.acquire()
                self.state_args = args[1]
                self.switchState(args[0])
                self.robot_state_lock.release()

    def switchState(self, next_state):
        """
        switches the state to a new state. The robot state lock must be acquired
        :param next_state: the next state
        """
        # make sure we are able toaccess the state safely
        if not self.robot_state_lock.locked():
            raise Exception(
                "Must Acquire robot state lock before calling this switchState!!!")
        # only change the state if it's different than the current state
        if self.state.getType() != next_state:
            # delete the previous state, if there is one
            if self.state is not None:
                print("changing from state " + self.state.getType().value +
                      " to state " + next_state.value)
                del self.state
            # update state to an instance of the new state
            self.state = self.makeState(next_state)

    def notify(self, topic, value):
        """
        notifies the state machine of info
        :param topic: the topic
        :param value: the value
        """

        # this default means don't change the state when we call determineNextState()
        args = None

        # if we are ESTOP, stop everything right away
        if topic == BehavioralStates_T.ESTOP:
            self.drive.stop()
            self.weapon.stop()
        if topic in IntelligenceStates_T:
            # if we are requesting to change the intelligence state
            if self.intelligence_state != topic:
                self.intelligence_state = topic
                # if in idle, switch to STOP, if in AUTO, also switch to STOP to stop prev state
                if topic == IntelligenceStates_T.IDLE or topic == IntelligenceStates_T.AUTO:
                    args = (BehavioralStates_T.STOP, "")
                elif topic == IntelligenceStates_T.RC:
                    args = (BehavioralStates_T.RC, ("", "0"))
        elif topic == SetJSONVars_T.DRIVE_ENABLE_CHANGE or topic == SetJSONVars_T.WEAPON_ENABLE_CHANGE:
            # Bypass state machine to send enabling info to the robot
            # There is no associated state
            self.wifi.sendInfo(topic.value, value)
        elif topic in BehavioralStates_T:
            self.robot_state_lock.acquire()
            curr_state = self.state.getType()
            curr_state_args = self.state_args
            self.robot_state_lock.release()
            # if anything has changed, request a state change
            if curr_state is None or curr_state_args is None or topic != curr_state or value != curr_state_args:
                args = (topic, value)
        self.determineNextState(args)
