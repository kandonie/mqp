from Hardware_Comms import WiFiComms
from Hardware_Comms import ESPHTTPTopics

class MotorCurrent:
    def __init__(self):
        self.drive_current = self.read()

    # read IMU heading
    def read(self):
        self.drive_current = WiFiComms.getInfo(ESPHTTPTopics.GetJSONVars.DRIVE_CURRENT)
        return self.drive_current
