from Guidance.GuidanceEnums import BehavioralStates
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

    def execute(self, robotData, stateArgs):
        """
        controls the robot based on which key is pressed/released
        :param robotData: the robot data (sensor info, CV, so on)
        :param stateArgs: the arguments for this state
        :return: True if the state is done and ready to transition to the next state, False otherwise
        """

        # TODO do something with basicGUI to create a pop-up box to input weapon speed
        # based on keyboard inputs, send corresponding drive and weapon signals
        key = stateArgs
        if key is not self.key:
            self.key = key
            self.keyMap(key)

    def keyMap(self, key):
        """
        commands the robot to do an action depending
        on the key pressed
        :param key: the key pressed
        """
        if key == Qt.Key_Up:
            # move robot forward
            # this might need reversing
            self.drive.driveSpeed(PWMVals.FULL_CCW.value)
        elif key == Qt.Key_Down:
            # move robot backward
            # this might need reversing
            self.drive.driveSpeed(PWMVals.FULL_CW.value)
        elif key == Qt.Key_Left:
            # rotate robot CCW
            # this might need reversing
            self.drive.turnSpeed(PWMVals.FULL_CCW.value)
        elif key == Qt.Key_Right:
            # rotate robot CW
            # this might need reversing
            self.drive.turnSpeed(PWMVals.FULL_CW.value)
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

        return False

    def getType(self):
        """
        :return: the the type of behavior state this is
        """
        return BehavioralStates.RC

    def getNextState(self):
        """
        Returns the state to transition to after this one
        :return: [(BehavioralState, (args...))] the next state as (state, stateArgs), or None for STOP
        """
        return None
