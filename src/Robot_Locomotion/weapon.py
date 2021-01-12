from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars_T
from src.Robot_Locomotion.MotorEnums import PWMVals_T


class Weapon:
    """the computer representation of the weapon
    """

    def __init__(self, wifi):
        """
        initilaize the weapon
        :param wifi: the wifi
        """
        self.wifi = wifi
        self.is_on = False

    def stop(self):
        """
        sets the weapon speed to 0
        """
        self.wifi.sendInfo(SetJSONVars_T.WEAPON_PWM.value, PWMVals_T.STOPPED.value)
        self.is_on = False

    def toggle(self):
        """
        turns the weapon on or off based on its current state
        """
        if not self.is_on:
            self.turnOn()
        else:
            self.stop()

    def turnOn(self):
        """
        turns the weapon on
        """
        self.wifi.sendInfo(SetJSONVars_T.WEAPON_PWM.value, PWMVals_T.FULL_CCW.value)
        self.is_on = True
