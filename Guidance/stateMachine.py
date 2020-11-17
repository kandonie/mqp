from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.GuidanceEnums import BehavioralStates, IntelligenceStates, RobotDataTopics
from Guidance.States.IdleState import IdleState
from Guidance.States.MovementTests import PolygonalMovement
from Guidance.States.PWMController import PWMController
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
        self.drive = Drive(wifi)
        self.weapon = Weapon(wifi)
        self.state = IdleState(self.drive, self.weapon)
        self.intelligenceState = IntelligenceStates.IDLE
        self.robotData = {}
        self.robotDataLock = threading.Lock()
        self.requestStateChange = False
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
        return state

    def determineNextState(self, args):
        """determines the next state of the robot 
        """
        if self.intelligenceState == IntelligenceStates.IDLE:
            self.switchState(BehavioralStates.ESTOP)
        elif self.intelligenceState == IntelligenceStates.RC:
            ##TODO teleop STUff
            pass
        elif self.intelligenceState == IntelligenceStates.AUTO:
            if self.requestStateChange:
                #switch to requested state
                if args is not None:
                    self.robotDataLock.acquire()
                    self.robotData[RobotDataTopics.BEHAVIOR_SPECIFIC_DATA] = args
                    self.switchState(self.robotData[RobotDataTopics.BEHAVIOR_SPECIFIC_DATA][0])
                    self.robotDataLock.release()
                    self.requestStateChange = False


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
        elif topic in BehavioralStates:
            data = self.robotData[RobotDataTopics.BEHAVIOR_SPECIFIC_DATA]
            if data is None or topic != data[0] or value != data[1]:
                self.requestStateChange = True
                args = (topic, value)

        self.determineNextState(args)