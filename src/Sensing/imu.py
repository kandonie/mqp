from src.Hardware_Comms import ESPHTTPTopics, WiFiComms
import threading
import time
# TODO @Kristen document
class IMU:

    def __init__(self, wifi):
        self.wifi = wifi
        self.heading = 0
        self.topic = ESPHTTPTopics.GetJSONVars.HEADING
        self.heading = self.read()

    # read IMU heading
    def read(self):
        while(True):
            try:
                self.heading = float(self.wifi.getInfo(self.topic))
                print("heading got")
            except:
                print("heading not got")
            time.sleep(5)
