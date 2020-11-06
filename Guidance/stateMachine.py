from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.states import States, IntelligenceStates
from Hardware_Comms.ESPHTTPTopics import CommsTopics, GetJSONVars

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
        self.state = States.MATCH_START
        self.sensors = []
        self.connectivity = None

        #make a dict of information needed to switch states
        self.infoDict = {"INTELLIGENCE_STATE" : IntelligenceStates.IDLE.value}
        for topic in GetJSONVars:
            self.infoDict[topic.value] = ""

        #used for switch case of states
        self.switcher = {
            States.MATCH_START: self.idle()
            }

    def runStateMachine(self):
        """exectutes states based on self.infoDict
        """
        self.switcher[self.state]

    def determineNextState(self):
        """determines the next state of the robot 
        """
        pass

    #this function gets called when there is new info
    def notify(self, topic, value):
        """called when observable has new info. Updates self.infoDict

        Args:
            topic (CommsTopics): the communication topic
            value (string): the value of the topic
        """
        if topic == CommsTopics.ESTOP:
            self.ESTOP()
        elif topic == CommsTopics.INTELLIGENCE_STATE:
            if value == IntelligenceStates.IDLE:
                self.state = States.ESTOP
            else:
                pass
        elif topic == CommsTopics.SET_PWM:
            self.drive.setPWM(value)

        self.determineNextState()

    def ESTOP(self):
        """stops all motors and puts the robot into ESTOP state
        """
        self.weapon.stop()
        self.drive.stop()
        self.state = States.ESTOP

    def idle(self):
        """makes the robot do nothing
        """
        pass