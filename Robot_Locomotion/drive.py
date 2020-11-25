from Hardware_Comms.ESPHTTPTopics import SetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals
import time

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
        self.wifi.sendInfo(SetJSONVars.MOTOR1_PWM.value, PWMVals.STOPPED.value)
        self.wifi.sendInfo(SetJSONVars.MOTOR2_PWM.value, PWMVals.STOPPED.value)

    def drive(self, speed):
        """drives stright at speed

        Args:
            speed (string): the speed to drive at
        """
        print("driving with PWM: " + str(speed))
        if int(speed) < 0:
            self.setPWM(SetJSONVars.MOTOR1_PWM.value, speed)
            self.setPWM(SetJSONVars.MOTOR2_PWM.value, speed)
        else:
            self.setPWM(SetJSONVars.MOTOR1_PWM.value, speed)
            self.setPWM(SetJSONVars.MOTOR2_PWM.value, speed)

    def turn(self, angle):
        """turns the robot to angle

        Args:
            angle (string): The global angle to turn to in degrees
        """
        print("Turning " + str(angle) + " degrees")
        if int(angle) > 0:
            self.setPWM(SetJSONVars.MOTOR1_PWM.value, PWMVals.FULL_CW.value)
            self.setPWM(SetJSONVars.MOTOR2_PWM.value, PWMVals.FULL_CCW.value)
        else:
            self.setPWM(SetJSONVars.MOTOR1_PWM.value, PWMVals.FULL_CCW.value)
            self.setPWM(SetJSONVars.MOTOR2_PWM.value, PWMVals.FULL_CW.value)



    def driveDistance(self, distance):
        print("Driving " + str(distance) + " meters")
        self.drive(1) #1m/s
        time.sleep(distance)
        self.stop()

    def setPWM(self, motor, pwm):
        """sets the pwm of drive motors

        Args:
            pwm (string): the pwm to set the motors to
        """
        self.wifi.sendInfo(motor, pwm)
