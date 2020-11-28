from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.GuidanceEnums import BehavioralStates, IntelligenceStates, RobotDataTopics
from Guidance.States.IdleState import IdleState
from Guidance.States.MovementTests import PolygonalMovement
from Guidance.States.PWMController import PWMController
from Guidance.States.RemoteControl import RemoteControl
from Hardware_Comms.ESPHTTPTopics import SetJSONVars
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
        self.state = IdleState(self.drive, self.weapon)
        self.intelligenceState = IntelligenceStates.IDLE
        self.robotData = {}
        self.robotDataLock = threading.Lock()
        for topic in RobotDataTopics:
            self.robotData[topic] = None

    def runStateMachine(self):
        """executes states based on current state
        """
        #TODO find better name
        while(1):
            #avoid reading from self.robotData while it is modified and state hasn't been update to match
            self.robotDataLock.acquire(True)
            self.state.execute(self.robotData)
            self.robotDataLock.release()

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
        if self.intelligenceState == IntelligenceStates.IDLE:
            self.switchState(BehavioralStates.ESTOP)
            print("psst  .... we are in IDLE. Change to auto to send robot messages")
        elif self.intelligenceState == IntelligenceStates.RC:
            ##TODO teleop STUff
            ##TODO keyboard up down left and right correspond to movement
            self.switchState(BehavioralStates.RC)
            print("psst .... we are in RC now!")
            print("Space bar for ESTOP")
            print("Up arrow key for drive forward\nDown arrow key for drive backward")
            print("Right arrow key for rotate CW\nLeft arrow key for rotate CCW")
            print("'w' key for toggle weapon on/off\n'/' key for stop drive motors")
        elif self.intelligenceState == IntelligenceStates.AUTO:
            #switch to requested state
            if args is not None:
                #TODO might want if args[0] in BehavioralStates if you have other things that change args in notify
                self.robotDataLock.acquire()
                #the folllowing line is here so don't change if in IDLE or RC
                self.robotData[RobotDataTopics.BEHAVIORAL_STATE] = args[0]
                self.robotData[RobotDataTopics.BEHAVIORAL_ARGS] = args[1]
                self.switchState(self.robotData[RobotDataTopics.BEHAVIORAL_STATE])
                self.robotDataLock.release()


    def switchState(self, nextState):
        if self.state.getType() != nextState:
            self.state = self.makeState(nextState)

    #this function gets called when there is new info
    def notify(self, topic, value):
        """called when observable has new info. Updates self.infoDict

        Args:
            topic (CommsTopics): the communication topic, can be StateDataTopics
            value (string): the value of the topic
        """
        #TODO account for don't switch if in ESTOP and Stuff like that
        args = None
        if topic in IntelligenceStates:
            self.intelligenceState = topic
        elif topic == SetJSONVars.ARM_DRIVE or topic == SetJSONVars.ARM_WEAPON:
            # TODO right now we bypass the state machine but maybe we don't want to?
            self.wifi.sendInfo(topic.value, value)
        elif topic in BehavioralStates:
            curr_state = self.robotData[RobotDataTopics.BEHAVIORAL_STATE]
            curr_state_args = self.robotData[RobotDataTopics.BEHAVIORAL_ARGS]
            #data is a tuple of (topic, value), ex: (BehavioralStates.PWM, (motor1, 1500))
            if curr_state is None or curr_state_args is None or topic != curr_state or value != curr_state_args:
                args = (topic, value)
        self.determineNextState(args)
