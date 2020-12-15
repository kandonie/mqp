from Hardware_Comms.ESPHTTPTopics import SetJSONVars, RobotMovementType
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
        # TODO might want to make wifi static methods
        self.wifi = wifi

    def stop(self):
        """sets the speeds of both motors to 0
        """
        self.wifi.sendInfo(SetJSONVars.MOTOR1_PWM.value, PWMVals.STOPPED.value)
        self.wifi.sendInfo(SetJSONVars.MOTOR2_PWM.value, PWMVals.STOPPED.value)
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.PWM_CONTROLLED)

    def driveSpeed(self, speed):
        """drives stright at speed

        Args:
            speed (string): the speed to drive at
        """
        print("driving with PWM: " + str(speed))
        if int(speed) > int(PWMVals.FULL_CW.value):
            speed = PWMVals.FULL_CW.value
        elif int(speed) < int(PWMVals.FULL_CCW.value):
            speed = PWMVals.FULL_CCW.value
        self.setPWM(SetJSONVars.MOTOR1_PWM.value, speed)
        self.setPWM(SetJSONVars.MOTOR2_PWM.value, speed)
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.PWM_CONTROLLED)

    def turnAngle(self, angle):
        """turns the robot to angle

        Args:
            angle (string): The global angle to turn to in degrees
        """
        print("Turning " + str(angle) + " degrees")
        self.wifi.sendInfo(SetJSONVars.DESIRED_HEADING.value, str(angle))
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.TURN_ANGLE)

    def turnSpeed(self, speed):
        """
        turns the robot at a speed
        Args:
            speed (string): The speed in pwm at which to rotate
        """
        if int(speed) > int(PWMVals.FULL_CW.value):
            speed = PWMVals.FULL_CW.value
        elif int(speed) < int(PWMVals.FULL_CCW.value):
            speed = PWMVals.FULL_CCW.value
        print("Turning speed")
        if int(speed) > int(PWMVals.STOPPED.value):
            invertedSpeed = int(speed) - int(PWMVals.STOPPED.value)
            invertedSpeed = str(int(PWMVals.STOPPED.value) - invertedSpeed)
            self.setPWM(SetJSONVars.MOTOR1_PWM.value, speed)
            self.setPWM(SetJSONVars.MOTOR2_PWM.value, invertedSpeed)
        else:
            invertedSpeed = int(PWMVals.STOPPED.value) - int(speed)
            invertedSpeed = str(invertedSpeed + int(PWMVals.STOPPED.value))
            self.setPWM(SetJSONVars.MOTOR1_PWM.value, speed)
            self.setPWM(SetJSONVars.MOTOR2_PWM.value, invertedSpeed)
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.PWM_CONTROLLED)

    def driveDistance(self, distance):
        print("Driving " + str(distance) + " meters")
        self.wifi.sendInfo(SetJSONVars.DESIRED_DISTANCE.value, str(distance))
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.DRIVE_DISTANCE)

    # TODO make a motor class that has this,cuz this is also appicable for weapon
    def setPWM(self, motor, pwm):
        """sets the pwm of drive motors

        Args:
            pwm (string): the pwm to set the motors to
        """
        self.wifi.sendInfo(motor, pwm)
