import requests
from Hardware_Comms.ESPHTTPTopics import GetJSONVars, SetJSONVars, HTTPTopics
from Hardware_Comms.connectionData import ConnectionDataHandler


class WiFiComms:
    """communiation over wifi"""
    def __init__(self):
        """initializes wifi connection and IP
        """        
        # esp32 IP
        self.IP = "http://192.168.49.241"
        #initialzies get vars
        self.getJson = {}
        for var in GetJSONVars:
            self.getJson[var.value] = '0'
        #initialize set vars
        self.setJson = {}
        for var in SetJSONVars:
            self.setJson[var.value] = '0'
        #determine is ESP is connected
        #if not done here, all http requests take forever and it slows down program
        try:
            print("Trying to connect to ESP...")
            requests.post(self.IP + HTTPTopics.MAIN.value, json=self.setJson)
            self.isConnected = True
            print("done!")
        except:
            print("failed")
            self.isConnected = False

        self.connectionHandler = ConnectionDataHandler()

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
            #TODO get the param
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
            return
        try:
            self.setJson[topic] = value
            response = requests.post(self.IP + HTTPTopics.MAIN.value, json=self.setJson)
            print(response)
            self.connectionHandler.execute(response.elapsed.total_seconds())
        except:
            print("No connection could be established with ESP")
            self.connectionHandler.loss()
            return "ESP Comms Err"
