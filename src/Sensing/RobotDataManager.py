from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, GetJSONVars


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

    def getRobotData(self):
        return self.robotData

    def notify(self, topic, value):
        # if we've had a change or is first time
        if not topic in self.robotData.keys() or \
                (topic in self.robotData.keys() and value != self.robotData[topic]):
            self.robotData[topic] = value
            self.notifyObservers(topic, value)
            self.checkForProblems()

    def checkForProblems(self):
        pass

    def notifyObservers(self, topic, value):
        for observer in self.observers:
            observer.notify(topic, value)

    def attachObserver(self, observer):
        self.observers.append(observer)


# WifiComms will notify RobotData, and RobotData needs to notify everyone else that something changed
# Singleton design pattern for RobotData, WifiComms

# This is going to check the robotData dict and based on what the values are, notify() stateMachine that
# a change in state (a topic!) is needed
#
# E.g.
# check the current, whoa look it's too high
# we need to go into back_off state
# notify() state machine and give it the back_off state topic
#
# E.g
# go into PWMController state with a specific speed
# call notify() state machine and give it the pwm controller topic with whatever speed as the value
#
# IMPORTANT NOTE:
# need to attach observers: stateMachine (maybe more later)
