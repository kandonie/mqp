from Hardware_Comms import WiFiComms
from Hardware_Comms import ESPHTTPTopics

class IMU:
    def __init__(self):
        self.heading = self.read()

    # read IMU heading
    def read(self):
        self.heading = WiFiComms.getInfo(ESPHTTPTopics.GetJSONVars.HEADING)
        return self.heading
