from Hardware_Comms.ESPHTTPTopics import SetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals


class Weapon:
    """the computer representation of the weapon
    """

    def __init__(self, wifi):
        """initilaizes the wifi

        Args:
            wifi (WiFiComms): wifi comms
        """
        self.wifi = wifi
        self.isOn = False

    def stop(self):
        """sets the weapon speed to 0
        """
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, PWMVals.STOPPED.value)
        self.isOn = False

    def toggle(self):
        """turns the weapon on or off based on its current state
        """
        if not self.isOn:
            self.turnOn()
        else:
            self.stop()

    def turnOn(self):
        """turns the weapon on
        """
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, PWMVals.FULL_CCW.value)
        self.isOn = True
