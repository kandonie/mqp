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

        #short circuit if bad args passed to RC, first arg is always "", so bad
        if len(stateArgs) <= 1:
            print("bad args for RC. Wanted (key, speed) but got " + str(stateArgs))
            self.first = False
            return False

        # based on keyboard inputs, send corresponding drive and weapon signals
        key = stateArgs[0]
        speed = int(stateArgs[1])
        if key is not self.key:
            self.key = key
            self.keyMap(key, speed)

    def keyMap(self, key, speed):
        """
        commands the robot to do an action depending
        on the key pressed
        :param key: the key pressed
        """
        if key == Qt.Key_Up:
            # move robot forward
            speed = int(PWMVals.STOPPED.value) - speed
            self.drive.driveSpeed(str(speed))
        elif key == Qt.Key_Down:
            # move robot backward
            speed = int(PWMVals.STOPPED.value) + speed
            self.drive.driveSpeed(str(speed))
        elif key == Qt.Key_Left:
            # rotate robot CCW
            speed = int(PWMVals.STOPPED.value) - speed
            self.drive.turnSpeed(int(speed))
        elif key == Qt.Key_Right:
            # rotate robot CW
            speed = int(PWMVals.STOPPED.value) + speed
            self.drive.turnSpeed(int(speed))
        elif key == Qt.Key_Slash:
            # stop drive
            self.drive.stop()
        elif key == Qt.Key_W:
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
