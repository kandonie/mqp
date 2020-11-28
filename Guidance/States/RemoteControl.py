from Guidance.GuidanceEnums import BehavioralStates
from Guidance.GuidanceEnums import RobotDataTopics
from Robot_Locomotion.MotorEnums import PWMVals
from PyQt5.Qt import Qt

class RemoteControl:

    def __init__(self, drive, weapon):
        """
        make robot controllable from keyboard
        create a pop-up box with the following instructions
            up arrow key for forward
            down arrow key for backward
            right arrow key for CW motion
            left arrow key for CCW motion
            space for stop drive
            w for toggle weapon on/off
            input box to input weapon pwm, that is saved across on/off toggles until changed
        :param drive:   [Drive]     Drive object to control robot drive motors
        :param weapon:  [Weapon]    Weapon object...to control robot weapon...
        """
        self.drive = drive
        self.weapon = weapon

        self.key = None


    def execute(self, robotData):
        """

        :param robotData: [{items in RobotDataTopics}]  RobotDataTopics.BEHAVIORAL_ARGS is in the dict and is a key press
        :return:
        """
        # self.drive.driveSpeed(PWMVals.FULL_CCW.value)
        #TODO do something with basicGUI to create a pop-up box to input weapon speed
        # based on keyboard inputs, send corresponding drive and weapon signals

        key = robotData[RobotDataTopics.BEHAVIORAL_ARGS]
        if key is not self.key:
            self.key = key
            self.keyMap(key)


    def keyMap(self, key):
        if key == Qt.Key_Up:
            # move robot forward
            # this might need reversing
            self.drive.driveSpeed(PWMVals.FULL_CW.value)
        elif key == Qt.Key_Down:
            # move robot backward
            # this might need reversing
            self.drive.driveSpeed(PWMVals.FULL_CCW.value)
        elif key == Qt.Key_Left:
            # rotate robot CCW
            # this might need reversing
            self.drive.turnSpeed(PWMVals.FULL_CW.value)
        elif key == Qt.Key_Right:
            # rotate robot CW
            # this might need reversing
            self.drive.turnSpeed(PWMVals.FULL_CCW.value)
        elif key == Qt.Key_Slash:
            # stop drive
            self.drive.stop()
        elif key == 'w':
            # toggle weapon on/off
            self.weapon.toggle()
        elif key == Qt.Key_Space:
            # ESTOP
            self.drive.stop()
            self.weapon.stop()


    def getType(self):
        return BehavioralStates.RC
