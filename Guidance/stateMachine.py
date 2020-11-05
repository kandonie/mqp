from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.states import States, IntelligenceStates
from Hardware_Comms.ESPHTTPTopics import CommsTopics, GetJSONVars

class StateMachine():
    def __init__(self, wifi):
        self.drive = Drive(wifi)
        self.weapon = Weapon(wifi)
        self.state = States.MATCH_START

        self.sensors = []
        self.connectivity = None
        self.infoDict = {"INTELLIGENCE_STATE" : IntelligenceStates.IDLE.value}
        for topic in GetJSONVars:
            self.infoDict[topic.value] = ""

        self.switcher = {
            States.MATCH_START: self.idle()
            }

    def runStateMachine(self):
        self.switcher[self.state]

    def determineNextState(self):
        #if self.statoos
        pass

    #this function gets called when there is new info
    def notify(self, topic, value):
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
        self.weapon.stop()
        self.drive.stop()
        self.state = States.ESTOP

    def idle(self):
        pass