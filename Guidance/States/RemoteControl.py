from Guidance.GuidanceEnums import BehavioralStates
from getkey import getkey, keys
from Robot_Locomotion.MotorEnums import PWMVals

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


    def execute(self, robotData):
        #TODO do something with basicGUI to create a pop-up box to input weapon speeds

        # based on keyboard inputs, send corresponding drive and weapon signals

        key = getkey()
        if key == keys.UP:
            # move robot forward
            # this might need reversing
            self.drive.driveSpeed(PWMVals.FULL_CW.value)
        elif key == keys.DOWN:
            # move robot backward
            # this might need reversing
            self.drive.driveSpeed(PWMVals.FULL_CCW.value)
        elif key == keys.LEFT:
            # rotate robot CCW
            # this might need reversing
            self.drive.turnSpeed(PWMVals.FULL_CW.value)
        elif key == keys.RIGHT:
            # rotate robot CW
            # this might need reversing
            self.drive.turnSpeed(PWMVals.FULL_CCW.value)
        elif key == keys.SLASH:
            # stop drive
            self.drive.stop()
        elif key == 'w':
            # toggle weapon on/off
            self.weapon.toggle()
        elif key == keys.SPACE:
            # ESTOP
            self.drive.stop()
            self.weapon.stop()


    def getType(self):
        return BehavioralStates.RC
