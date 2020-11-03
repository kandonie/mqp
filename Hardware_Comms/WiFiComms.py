import requests
from Hardware_Comms.ESPHTTPTopics import GetJSONVars, SetJSONVars, HTTPTopics


class WiFiComms:
    def __init__(self):
        # esp32 IP
        self.IP = "http://192.168.0.17"
        self.getJson = {}
        for var in GetJSONVars:
            self.getJson[var.name] = ''
        self.setJson = {}
        for var in SetJSONVars:
            self.setJson[var.name] = ''


    def getInfo(self, param):
        print("Notifying of " + str(param))
        # sending get request and saving the response as response object
        try:
            print("Before Request")
            r = requests.get(url=self.IP + str(param))
            print("After Request")
            print(r.content)
            return r.content
        except:
            print("No connection could be established with ESP")
            return "ESP Comms Err"

    def sendInfo(self, topic, value):
        print("asking " + str(value) + " of " + str(topic))
        try:
            #self.getInfo(HTTPTopics.MAIN.value) test line
            self.setJson[topic] = value
            response = requests.post(self.IP + HTTPTopics.MAIN.value, json=self.setJson)
            print(response)
        except:
            print("No connection could be established with ESP")
            return "ESP Comms Err"