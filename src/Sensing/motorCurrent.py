from src.Hardware_Comms import ESPHTTPTopics, WiFiComms


# TODO @Kristen Document

class MotorCurrent:
    def __init__(self):
        self.drive_current = self.read()
        self.topic = ESPHTTPTopics.GetJSONVars_T.DRIVE_CURRENT
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
