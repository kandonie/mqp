from Guidance.GuidanceEnums import BehavioralStates

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
        #TODO do something with basicGUI to create a pop-up box

        # gets keyboard inputs
        # based on keyboard inputs, send corresponding drive and weapon signals
        pass


    def getType(self):
        return BehavioralStates.RC
