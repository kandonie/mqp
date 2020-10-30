from Hardware_Comms.ESPHTTPTopics import SetJSONVars

class Weapon:
    def __init__(self, wifi):
        self.wifi = wifi

    def stop(self):
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.name, 0)

    def setPWM(self, pwm):
        self.wifi.sendInfo(SetJSONVars.WEAPON_PWM.name, pwm)