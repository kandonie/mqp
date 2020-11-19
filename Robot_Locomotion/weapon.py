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

    def stop(self):
        """sets the weapon speed to 0
        """
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, PWMVals.STOPPED.value)

    def toggle(self, isOn):
        """turns the weapon on or off 

        Args:
            isOn (bool): if isOn, set the weapon on, else, turn weapon off
        """
        if isOn:
            self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, PWMVals.FULL_CCW.value)
        else:
            self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, PWMVals.STOPPED.value)