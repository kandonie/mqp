from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.GuidanceEnums import BehavioralStates, IntelligenceStates
from Guidance.States.IdleState import IdleState
from Guidance.States.MovementTests import PolygonalMovement
from Guidance.States.PWMController import PWMController
from Guidance.States.RemoteControl import RemoteControl
from Hardware_Comms.ESPHTTPTopics import SetJSONVars, GetJSONVars
import threading

class StateMachine():
    """controls the decisions of the robot.
    """
    def __init__(self, wifi):
        """initializes variables

        Args:
            wifi (WiFiComms): The wifi object used to communicate with the robot
        """
        #init vars
        self.wifi = wifi
        #set initial arm state to disarm
        #TODO maybe put this somewhere else
        self.wifi.sendInfo(SetJSONVars.ARM_WEAPON.value, "false")
        self.wifi.sendInfo(SetJSONVars.ARM_DRIVE.value, "false")
        self.drive = Drive(wifi)
        self.weapon = Weapon(wifi)
        self.state = self.makeState(BehavioralStates.ESTOP)
        self.stateArgs = None
        self.intelligenceState = IntelligenceStates.IDLE
        # robotData is a dict with Behavioral_Args and Behavioral_State
        self.robotData = {}
        self.robotDataLock = threading.Lock()
        self.robotStateLock = threading.Lock()
        for topic in SetJSONVars:
            self.robotData[topic] = None

    def runStateMachine(self):
        """executes states based on current state
        """
        #TODO find better name
        while True:
            #avoid reading from self.robotData while it is modified and state hasn't been update to match
            self.robotDataLock.acquire()
            data = self.robotData
            self.robotDataLock.release()

            self.robotStateLock.acquire()
            done_state = self.state.execute(data, self.stateArgs)
            self.robotStateLock.release()

            if done_state:
                new_state_with_args = self.state.getNextState()
                if new_state_with_args == None:
                    new_state_with_args = (BehavioralStates.ESTOP, None)
                self.determineNextState(new_state_with_args)



    def makeState(self, state):
        if state == BehavioralStates.ESTOP:
            state = IdleState(self.drive, self.weapon)
        elif state == BehavioralStates.MOVEMENT_TEST:
            state = PolygonalMovement(self.drive)
        elif state == BehavioralStates.PWM:
            state = PWMController(self.drive)
        elif state == BehavioralStates.RC:
            state = RemoteControl(self.drive, self.weapon)
        return state

    def determineNextState(self, args):
        """determines the next state of the robot 
        """
        if args is not None and len(args) == 2:
            if self.intelligenceState == IntelligenceStates.IDLE:
                #don't change the behavioral state if in IDLE
                print("psst  .... we are in IDLE. Change to auto to send robot messages")
            else:
                self.robotStateLock.acquire()
                self.stateArgs = args[1]
                self.switchState(args[0])
                self.robotStateLock.release()

    ###need to acquire state lock before calling
    def switchState(self, nextState):
        if not self.robotStateLock.locked():
            raise Exception("Must Acquire robot state lock before calling this switchState!!!")
        if self.state.getType() != nextState:
            if self.state is not None:
                print("changing from state " + self.state.getType().value + " to state " + nextState.value)
                del self.state
            self.state = self.makeState(nextState)

    #this function gets called when there is new info
    def notify(self, topic, value):
        """called when observable has new info. Updates self.infoDict

        Args:
            topic (CommsTopics): the communication topic, typically an enum
            value (string): the value of the topic
        """
        #TODO account for don't switch if in ESTOP and Stuff like that
        #TODO edge case for race cases with mux
        args = None
        if topic in IntelligenceStates:
            #if we are requesting to change the state
            if self.intelligenceState != topic:
                self.intelligenceState = topic
                #if in idle, switch to ESTOP, if in AUTO, also switch to ESTOP to stop prev state
                if topic == IntelligenceStates.IDLE or topic == IntelligenceStates.AUTO:
                    args = (BehavioralStates.ESTOP, "")
                elif topic == IntelligenceStates.RC:
                    args = (BehavioralStates.RC, "")
        elif topic == SetJSONVars.ARM_DRIVE or topic == SetJSONVars.ARM_WEAPON:
            ##Bypass state machine to send arming info to the robot
            self.wifi.sendInfo(topic.value, value)
        elif topic in BehavioralStates:
            #TODO Figure out Mux
            self.robotStateLock.acquire()
            curr_state = self.state.getType()
            curr_state_args = self.stateArgs
            self.robotStateLock.release()
            #data is a tuple of (topic, value), ex: (BehavioralStates.PWM, (motor1, 1500))
            if curr_state is None or curr_state_args is None or topic != curr_state or value != curr_state_args:
                args = (topic, value)
        elif topic in GetJSONVars:
            self.robotDataLock.acquire()
            self.robotData[topic] = value
            self.robotDataLock.release()
        self.determineNextState(args)
