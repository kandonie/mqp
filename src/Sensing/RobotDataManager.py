from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars_T, GetJSONVars_T
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
            for topic in SetJSONVars_T:
                self.robotData[topic] = None
            for topic in GetJSONVars_T:
                self.robotData[topic] = None
            self.observers = []
            self.robot_data_lock = threading.Lock()

    def getRobotData(self):
        self.robot_data_lock.acquire(True)
        data = self.robotData
        self.robot_data_lock.release()
        return data

    def notify(self, topic, value):
        # if we've had a change or is first time
        self.robot_data_lock.acquire(True)
        if not topic in self.robotData.keys() or value != self.robotData[topic]:
            self.robotData[topic] = value
            self.robot_data_lock.release()
            self.notifyObservers(topic, value)
            self.checkForProblems()
        else:
            self.robot_data_lock.release()

    def checkForProblems(self):
        #TODO
        #if bad connection
            #bad conn state
        #elif robot upside donw
            #Right self state
        #elif weapon curr too high / motor can't move
            #back off
        #elif weapon malfuntion/stall
           #weapon malfunction state?
        pass

    def notifyObservers(self, topic, value):
        for observer in self.observers:
            observer.notify(topic, value)

    def attachObserver(self, observer):
        self.observers.append(observer)