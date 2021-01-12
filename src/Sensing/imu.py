from src.Hardware_Comms import ESPHTTPTopics, WiFiComms


# TODO @Kristen document
class IMU:
    def __init__(self):
        self.heading = self.read()
        self.topic = ESPHTTPTopics.GetJSONVars_T.HEADING
        self.observers = []

    # read IMU heading
    def read(self):
        self.heading = WiFiComms.getInfo(self.topic)
        self.notifyObservers()

    def notifyObservers(self):
        for observer in self.observers:
            observer.notify(self.topic, self.heading)

    def attachObservers(self, observers):
        for observer in observers:
            self.observers.append(observer)
