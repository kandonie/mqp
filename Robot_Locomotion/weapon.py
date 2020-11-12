from Hardware_Comms.ESPHTTPTopics import SetJSONVars

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
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, 0)

    def toggle(self, isOn):
        """turns the weapon on or off 

        Args:
            isOn (bool): if isOn, set the weapon on, else, turn weapon off
        """
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, isOn)