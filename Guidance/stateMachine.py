from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.observer import Observer
from Guidance.states import States
from Hardware_Comms.ESPHTTPTopics import StateMachineTopics
from Guidance.IntelligenceState import IntelligenceState

class StateMachine(Observer):
    def __init__(self, wifi):
        self.drive = Drive(wifi)
        self.weapon = Weapon(wifi)
        self.state = States.IDLE

    def notify(self, topic, value):
        if topic == StateMachineTopics.ESTOP:
            self.ESTOP()
        elif topic == StateMachineTopics.INTELLIGENCE_STATE:
            if value == IntelligenceState.STOPPED:
                self.state = States.IDLE
            else:
                pass
        elif topic == StateMachineTopics.SET_PWM:
            self.drive.setPWM(value)


    def ESTOP(self):
        self.weapon.stop()
        self.drive.stop()
        self.state = States.IDLE ##################should I make estop state?

