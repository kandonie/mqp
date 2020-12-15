import requests
from Hardware_Comms.ESPHTTPTopics import GetJSONVars, SetJSONVars, HTTPTopics
from Hardware_Comms.connectionData import ConnectionDataHandler
from Robot_Locomotion.MotorEnums import PWMVals


class WiFiComms:
    """communiation over wifi"""

    def __init__(self, shouldConnectToWiFi):
        """initializes wifi connection and IP
        """
        # esp32 IP
        self.IP = "http://192.168.50.129"
        # initialzies get vars
        self.getJson = {}
        for var in GetJSONVars:
            self.getJson[var.value] = PWMVals.STOPPED.value
        # initialize set vars
        self.setJson = {}
        for var in SetJSONVars:
            self.setJson[var.value] = PWMVals.STOPPED.value
        # determine is ESP is connected
        # if not done here, all http requests take forever and it slows down program
        if shouldConnectToWiFi == True:
            try:
                print("Trying to connect to ESP...")
                requests.post(self.IP + HTTPTopics.MAIN.value, json=self.setJson)
                self.isConnected = True
                print("done!")
            except:
                print("failed")
                self.isConnected = False
        else:
            self.isConnected = False

        self.connectionHandler = ConnectionDataHandler()
        self.observers = []

    def getInfo(self, param):
        """does a get request for get json vars

        Args:
            param (GetJSONVars): The topic to ask for

        Returns:
            string: topic information
        """
        print("Notifying of " + str(param))
        if not self.isConnected:
            return "No ESP Connected"
        # sending get request and saving the response as response object
        try:
            r = requests.get(url=self.IP + HTTPTopics.MAIN.value)
            # TODO get the param
            return r.content
        except:
            print("No connection could be established with ESP")
            return "ESP Comms Err"

    def sendInfo(self, topic, value):
        """sets values over wifi

        Args:
            topic (SetJSONVars): the topic to set
            value (String): the value to set for the topic
        """
        print("asking " + str(value) + " of " + str(topic))
        if not self.isConnected:
            self.notifyObservers(GetJSONVars.HEADING, "100")
            return
        try:
            self.setJson[topic] = value
            response = requests.post(self.IP + HTTPTopics.MAIN.value, json=self.setJson)
            self.parseResponse(response)
            self.connectionHandler.execute(response.elapsed.total_seconds())
        except:
            print("No connection could be established with ESP")
            self.connectionHandler.loss()
            return "ESP Comms Err"

    def parseResponse(self, response):
        print(response)
        # for item in response
        # if diff from self.GetJSON
        # change val in self.GETJSON
        # notify observers

    def notifyObservers(self, topic, value):
        for observer in self.observers:
            observer.notify(topic, value)

    def attachObserver(self, observer):
        self.observers.append(observer)
