from Hardware_Comms.ESPHTTPTopics import SetJSONVars

class Weapon:
    def __init__(self, wifi):
        self.wifi = wifi

    def stop(self):
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, 0)

    def toggle(self, isOn):
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.value, isOn)