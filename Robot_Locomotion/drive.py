from Hardware_Comms.ESPHTTPTopics import SetJSONVars

class Drive:
    def __init__(self, wifi):
        self.wifi = wifi

    def stop(self):
        self.wifi.sendInfo(SetJSONVars.MOTOR1_PWM.value, 0)

    def drive(self, speed):
        pass

    def turn(self, angle):
        pass

    def setPWM(self, pwm):
        self.wifi.sendInfo(SetJSONVars.MOTOR1_PWM.value, pwm)
        self.wifi.sendInfo(SetJSONVars.MOTOR2_PWM.value, pwm)
