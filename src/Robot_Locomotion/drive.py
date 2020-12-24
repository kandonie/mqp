from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, RobotMovementType
from src.Robot_Locomotion.MotorEnums import PWMVals


class Drive:
    """
    the computer representation of the drive
    """

    def __init__(self, wifi):
        """
        initializes drive
        :param wifi:  the wifi
        """
        self.wifi = wifi

    def stop(self):
        """
        sets the speeds of both motors to 0
        """
        self.wifi.sendInfo(SetJSONVars.MOTOR1_PWM.value, PWMVals.STOPPED.value)
        self.wifi.sendInfo(SetJSONVars.MOTOR2_PWM.value, PWMVals.STOPPED.value)
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.PWM_CONTROLLED)

    def driveSpeed(self, speed):
        """
        drives stright at speed
        :param speed: [String] the speed to drive at
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
        """
        turns the robot to angle
        :param angle: [String] The relative angle to turn to in degrees
        """
        print("Turning " + str(angle) + " degrees")
        self.wifi.sendInfo(SetJSONVars.DESIRED_HEADING.value, str(angle))
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.TURN_ANGLE)

    def turnSpeed(self, speed):
        """
        turns the robot at a speed
        :param speed: [String] The speed in pwm at which to rotate
        """

        # check bounds
        if int(speed) > int(PWMVals.FULL_CW.value):
            speed = PWMVals.FULL_CW.value
        elif int(speed) < int(PWMVals.FULL_CCW.value):
            speed = PWMVals.FULL_CCW.value

        print("Turning speed")
        # direction
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
        # start this movement type
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.PWM_CONTROLLED)

    def driveDistance(self, distance):
        """
        drives a distance
        :param distance: [int] the distance in meters
        """
        print("Driving " + str(distance) + " meters")
        self.wifi.sendInfo(SetJSONVars.DESIRED_DISTANCE.value, str(distance))
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.DRIVE_DISTANCE)

    def setPWM(self, motor, pwm):
        """
        sets the pwm of drive motors
        :param motor: the motor
        :param pwm:  the pwm
        """
        self.wifi.sendInfo(motor, pwm)