from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, RobotMovementType
from src.Guidance.GuidanceEnums import BehavioralStates
from src.CV.CVTopics import CVTopics
import threading


class Robot:
    """
    the computer representation of the drive
    """

    def __init__(self, wifi, drive, weapon):
        """
        initializes drive
        :param wifi:  the wifi
        """
        self.wifi = wifi
        self.drive = drive
        self.weapon = weapon
        self.observers = [self.drive]
        self.CVData = {}
        for item in CVTopics:
            self.CVData[item] = 0
        self.robotLock = threading.Lock()

    def disable(self):
        self.wifi.sendInfo(SetJSONVars.MOVEMENT_TYPE.value, RobotMovementType.DISABLE_ROBOT.value)

    def estop(self):
        self.wifi.getInfo("ESTOP")

    def getCVData(self, param):
        return self.CVData[param]

    def notify(self, topic, value):
        # if we've had a change or is first time
        self.robotLock.acquire(True)
        if value != self.CVData[topic]:
            self.CVData[topic] = value
            self.robotLock.release()
            self.notifyObservers(topic, value)
        else:
            self.robotLock.release()

    def notifyObservers(self, topic, value):
        """
        notify observers of change
        :param topic: the topic
        :param value: the value
        """
        for observer in self.observers:
            observer.notify(topic, value)
