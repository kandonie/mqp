from Hardware_Comms import WiFiComms
from Hardware_Comms import ESPHTTPTopics

class MotorCurrent:
    def __init__(self):
        self.drive_current = self.read()
        self.topic = ESPHTTPTopics.GetJSONVars.DRIVE_CURRENT
        self.observers = []

    # read IMU heading
    def read(self):
        self.drive_current = WiFiComms.getInfo(self.topic)
        self.notifyObservers()

    def notifyObservers(self):
        for observer in self.observers:
            observer.notify(self.topic, self.drive_current)

    def attachObservers(self, observers):
        for observer in observers:
            self.observers.append(observer)
