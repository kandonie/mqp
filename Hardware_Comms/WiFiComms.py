import requests
from Hardware_Comms.ESPHTTPTopics import GetJSONVars, SetJSONVars, HTTPTopics


class WiFiComms:
    def __init__(self):
        # esp32 IP
        self.IP = "http://192.168.4.1"
        self.getJson = {}
        for var in GetJSONVars:
            self.getJson[var.name] = ''
        self.setJson = {}
        for var in SetJSONVars:
            self.setJson[var.name] = ''


    def getInfo(self, param):
        print("Notifying of " + param)
        # sending get request and saving the response as response object
        try:
            r = requests.get(url=self.IP + str(param))
            print(r.content)
            return r.content
        except:
            print("No connection could be established with ESP")
            return "ESP Comms Err"

    def sendInfo(self, topic, value):
        print("asking " + str(value) + " of " + str(topic))
        try:
            self.setJson[topic] = value
            response = requests.post(self.IP + HTTPTopics.MAIN, json=self.setJson)
            print(response.json())
        except:
            print("No connection could be established with ESP")
            return "ESP Comms Err"