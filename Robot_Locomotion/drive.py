from Hardware_Comms.ESPHTTPTopics import SetJSONVars

class Drive:
    """the computer representation of the drive
    """
    def __init__(self, wifi):
        """initialized the wifi

        Args:
            wifi (WiFiComms): a wifi commms
        """
        #TODO might want to make wifi static methods
        self.wifi = wifi

    def stop(self):
        """sets the speeds of both motors to 0
        """
        self.wifi.sendInfo(SetJSONVars.MOTOR1_PWM.value, 0)
        self.wifi.sendInfo(SetJSONVars.MOTOR2_PWM.value, 0)

    def drive(self, speed):
        """drives stright at speed

        Args:
            speed (string): the speed to drive at
        """
        pass

    def turn(self, angle):
        """turns the robot to angle

        Args:
            angle (string): The global angle to turn to in degrees
        """
        pass

    def square(self, sideLen):
        pass

    def driveDistance(self, distance):
        pass

    def setPWM(self, pwm):
        """sets the pwm of drive motors

        Args:
            pwm (string): the pwm to set the motors to
        """
        self.wifi.sendInfo(SetJSONVars.MOTOR1_PWM.value, pwm)
        self.wifi.sendInfo(SetJSONVars.MOTOR2_PWM.value, pwm)
