from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars_T, RobotMovementType_T
from src.Robot_Locomotion.MotorEnums import PWMVals_T


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
        self.wifi.sendInfo(SetJSONVars_T.MOTOR1_PWM.value, PWMVals_T.STOPPED.value)
        self.wifi.sendInfo(SetJSONVars_T.MOTOR2_PWM.value, PWMVals_T.STOPPED.value)
        self.wifi.sendInfo(SetJSONVars_T.MOVEMENT_TYPE.value, RobotMovementType_T.PWM_CONTROLLED)

    def driveSpeed(self, speed):
        """
        drives stright at speed
        :param speed: [String] the speed to drive at
        """
        print("driving with PWM: " + str(speed))
        if int(speed) > int(PWMVals_T.FULL_CW.value):
            speed = PWMVals_T.FULL_CW.value
        elif int(speed) < int(PWMVals_T.FULL_CCW.value):
            speed = PWMVals_T.FULL_CCW.value
        self.setPWM(SetJSONVars_T.MOTOR1_PWM.value, speed)
        self.setPWM(SetJSONVars_T.MOTOR2_PWM.value, speed)
        self.wifi.sendInfo(SetJSONVars_T.MOVEMENT_TYPE.value, RobotMovementType_T.PWM_CONTROLLED)

    def turnAngle(self, angle):
        """
        turns the robot to angle
        :param angle: [String] The relative angle to turn to in degrees
        """
        print("Turning " + str(angle) + " degrees")
        self.wifi.sendInfo(SetJSONVars_T.DESIRED_HEADING.value, str(angle))
        self.wifi.sendInfo(SetJSONVars_T.MOVEMENT_TYPE.value, RobotMovementType_T.TURN_ANGLE)

    def turnSpeed(self, speed):
        """
        turns the robot at a speed
        :param speed: [String] The speed in pwm at which to rotate
        """

        # check bounds
        if int(speed) > int(PWMVals_T.FULL_CW.value):
            speed = PWMVals_T.FULL_CW.value
        elif int(speed) < int(PWMVals_T.FULL_CCW.value):
            speed = PWMVals_T.FULL_CCW.value

        print("Turning speed")
        # direction
        if int(speed) > int(PWMVals_T.STOPPED.value):
            inverted_speed = int(speed) - int(PWMVals_T.STOPPED.value)
            inverted_speed = str(int(PWMVals_T.STOPPED.value) - inverted_speed)
            self.setPWM(SetJSONVars_T.MOTOR1_PWM.value, speed)
            self.setPWM(SetJSONVars_T.MOTOR2_PWM.value, inverted_speed)
        else:
            inverted_speed = int(PWMVals_T.STOPPED.value) - int(speed)
            inverted_speed = str(inverted_speed + int(PWMVals_T.STOPPED.value))
            self.setPWM(SetJSONVars_T.MOTOR1_PWM.value, speed)
            self.setPWM(SetJSONVars_T.MOTOR2_PWM.value, inverted_speed)
        # start this movement type
        self.wifi.sendInfo(SetJSONVars_T.MOVEMENT_TYPE.value, RobotMovementType_T.PWM_CONTROLLED)

    def driveDistance(self, distance):
        """
        drives a distance
        :param distance: [int] the distance in meters
        """
        print("Driving " + str(distance) + " meters")
        self.wifi.sendInfo(SetJSONVars_T.DESIRED_DISTANCE.value, str(distance))
        self.wifi.sendInfo(SetJSONVars_T.MOVEMENT_TYPE.value, RobotMovementType_T.DRIVE_DISTANCE)

    def setPWM(self, motor, pwm):
        """
        sets the pwm of drive motors
        :param motor: the motor
        :param pwm:  the pwm
        """
        self.wifi.sendInfo(motor, pwm)
