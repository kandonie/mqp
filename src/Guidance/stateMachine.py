from src.Robot_Locomotion.drive import Drive
from src.Robot_Locomotion.weapon import Weapon
from src.Robot_Locomotion.robot import Robot
from src.Guidance.GuidanceEnums import BehavioralStates, IntelligenceStates
from src.Guidance.States.stop import Stop
from src.Guidance.States.PolygonalMovement import PolygonalMovement
from src.Guidance.States.PWMController import PWMController
from src.Guidance.States.RemoteControl import RemoteControl
from src.Guidance.States.match_start import MatchStart
from src.Guidance.States.EndMatch import MatchEnd
from src.Guidance.States.ESTOP import ESTOP
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, GetJSONVars
import threading
from src.Sensing.RobotDataManager import RobotDataManager


class StateMachine():
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
        self.wifi.sendInfo(SetJSONVars.WEAPON_ENABLE_CHANGE.value, "false")
        self.wifi.sendInfo(SetJSONVars.DRIVE_ENABLE_CHANGE.value, "false")
        self.drive = Drive(wifi)
        self.weapon = Weapon(wifi)
        self.robot = Robot(self.wifi, self.drive, self.weapon)
        self.state = self.makeState(BehavioralStates.STOP)
        self.stateArgs = None
        self.intelligenceState = IntelligenceStates.IDLE
        # robotData is a dict with Behavioral_Args and Behavioral_State
        self.robotDataManager = RobotDataManager.getInstance()
        self.robotDataManager.attachObserver(self)
        # locks for accessing state
        self.robotStateLock = threading.Lock()

    def runStateMachine(self):
        """
        executes states based on current state
        """
        while True:
            # get a copy of the current robot data
            data = self.robotDataManager.getRobotData()

            # execute state with that data
            self.robotStateLock.acquire()
            done_state = self.state.execute(data, self.stateArgs)
            self.robotStateLock.release()

            # when we are ready to go to the next state
            if done_state:
                new_state_with_args = self.state.getNextState()
                # none is a default option
                if new_state_with_args == None:
                    new_state_with_args = (BehavioralStates.STOP, None)
                self.determineNextState(new_state_with_args)

    def makeState(self, state):
        """
        makes an instance of the next state
        :param state: the next state
        :return: the new state
        """
        if state == BehavioralStates.STOP:
            state = Stop(self.drive, self.weapon)
        elif state == BehavioralStates.MOVEMENT_TEST:
            state = PolygonalMovement(self.drive)
        elif state == BehavioralStates.PWM:
            state = PWMController(self.drive)
        elif state == BehavioralStates.RC:
            state = RemoteControl(self.drive, self.weapon)
        elif state == BehavioralStates.ESTOP:
            state = ESTOP(self.robot)
        elif state == BehavioralStates.MATCH_START:
            state = MatchStart()
        elif state == BehavioralStates.END_MATCH:
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
            if self.intelligenceState == IntelligenceStates.IDLE and args[0] != BehavioralStates.ESTOP:
                # if we aren't in stop state, change to stop state, otherwise do nothing in IDLE
                if self.state.getType() != BehavioralStates.STOP:
                    self.robotStateLock.acquire()
                    self.switchState(BehavioralStates.STOP)
                    self.robotStateLock.release()
                print("psst  .... we are in IDLE. Change to auto to send robot messages")
            else:
                # change the state
                self.robotStateLock.acquire()
                self.stateArgs = args[1]
                self.switchState(args[0])
                self.robotStateLock.release()

    def switchState(self, nextState):
        """
        switches the state to a new state. The robot state lock must be acquired
        :param nextState: the next state
        """
        # make sure we are able toaccess the state safely
        if not self.robotStateLock.locked():
            raise Exception(
                "Must Acquire robot state lock before calling this switchState!!!")
        # only change the state if it's different than the current state
        if self.state.getType() != nextState:
            # delete the previous state, if there is one
            if self.state is not None:
                print("changing from state " + self.state.getType().value +
                      " to state " + nextState.value)
                del self.state
            # update state to an instance of the new state
            self.state = self.makeState(nextState)

    def notify(self, topic, value):
        """
        notifies the state machine of info
        :param topic: the topic
        :param value: the value
        """

        # this default means don't change the state when we call determineNextState()
        args = None

        # if we are ESTOP, stop everything right away
        if topic == BehavioralStates.ESTOP:
            self.drive.stop()
            self.weapon.stop()
        if topic in IntelligenceStates:
            # if we are requesting to change the intelligence state
            if self.intelligenceState != topic:
                self.intelligenceState = topic
                # if in idle, switch to STOP, if in AUTO, also switch to STOP to stop prev state
                if topic == IntelligenceStates.IDLE or topic == IntelligenceStates.AUTO:
                    args = (BehavioralStates.STOP, "")
                elif topic == IntelligenceStates.RC:
                    args = (BehavioralStates.RC, ("", "0"))
        elif topic == SetJSONVars.DRIVE_ENABLE_CHANGE or topic == SetJSONVars.WEAPON_ENABLE_CHANGE or topic == SetJSONVars.MOVEMENT_TYPE :
            # Bypass state machine to send enabling info to the robot
            # There is no associated state
            self.wifi.sendInfo(topic.value, value)
        elif topic in BehavioralStates:
            self.robotStateLock.acquire()
            curr_state = self.state.getType()
            curr_state_args = self.stateArgs
            self.robotStateLock.release()
            # if anything has changed, request a state change
            if curr_state is None or curr_state_args is None or topic != curr_state or value != curr_state_args:
                args = (topic, value)
        self.determineNextState(args)
