from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, GetJSONVars
import threading

class RobotDataManager:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RobotDataManager.__instance == None:
            RobotDataManager()
        return RobotDataManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if RobotDataManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            RobotDataManager.__instance = self
            # robotData is filled from WifiComms when it notifies RobotData (which means we need a notify() in this class
            self.robotData = {}
            for topic in SetJSONVars:
                self.robotData[topic] = None
            for topic in GetJSONVars:
                self.robotData[topic] = None
            self.observers = []
            self.robotDataLock = threading.Lock()

    def getRobotData(self):
        self.robotDataLock.acquire(True)
        data = self.robotData
        self.robotDataLock.release()
        return data

    def notify(self, topic, value):
        # if we've had a change or is first time
        self.robotDataLock.acquire(True)
        if not topic in self.robotData.keys() or value != self.robotData[topic]:
            self.robotData[topic] = value
            self.robotDataLock.release()
            self.notifyObservers(topic, value)
            self.checkForProblems()
        else:
            self.robotDataLock.release()

    def checkForProblems(self):
        pass

    def notifyObservers(self, topic, value):
        for observer in self.observers:
            observer.notify(topic, value)

    def attachObserver(self, observer):
        self.observers.append(observer)