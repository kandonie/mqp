from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.observer import Observer
from Guidance.states import States

class StateMachine(Observer):
    def __init__(self):
        self.drive = Drive()
        self.weapon = Weapon()
        self.state = States.IDLE