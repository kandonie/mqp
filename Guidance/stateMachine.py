from Robot_Locomotion.drive import Drive
from Robot_Locomotion.weapon import Weapon
from Guidance.observer import Observer
from Guidance.states import States
from GUI.buttonStrings import ButtonStrings

class StateMachine(Observer):
    def __init__(self):
        self.drive = Drive()
        self.weapon = Weapon()
        self.state = States.IDLE

    def update(self, data):
        data = self.parseData(data)
        if data == ButtonStrings.CCW_SQUARE:
            self.state = States.TEST_SQUARE_CCW
        elif data == ButtonStrings.CW_SQUARE:
            self.state = States.TEST_SQUARE_CW
        elif data == ButtonStrings.CW_TURN:
            self.state = States.TEST_TURN_CW
        elif data == ButtonStrings.CCW_TURN:
            self.state = States.TEST_TURN_CCW

        self.executeState()
    
    def executeState(self):
        if self.state == States.TEST_TURN_CCW:
            self.doFourRightAndleTurnsCCW
        elif self.state == States.TEST_TURN_CW:
            self.doFourRightAngleTurnsCW
        elif self.state == States.TEST_SQUARE_CCW:
            self.doSquareCCW
        elif self.state == States.TEST_SQUARE_CW:
            self.doSquareCW
        
        
    def parseData(self, data):
        return data

    def doSquareCW(self):
        sideLen = 10#feet
        for side in range(0,4):
            self.drive.driveStraight(sideLen)
            self.drive.turn(-90)

    def doSquareCCW(self):
        sideLen = 10#feet
        for side in range(0,4):
            self.drive.driveStraight(sideLen)
            self.drive.turn(90)

    def doFourRightAndleTurnsCCW(self):
        for i in range(0,4):
            self.drive.turn(90)

    def doFourRightAngleTurnsCW(self):
        for i in range(0,4):
            self.drive.turn(-90)
