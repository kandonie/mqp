import requests

class WiFiComms:
    def __init__(self):
        # esp32 IP
        self.IP = "http://192.168.4.1"


    def getInfo(self, param):
        # sending get request and saving the response as response object
        try:
            r = requests.get(url=self.IP + str(param))
            print(r.content)
            return r.content
        except:
            print("No connection could be established with ESP")
            return "ESP Comms Err"

    def sendInfo(self, info, param):
        pass