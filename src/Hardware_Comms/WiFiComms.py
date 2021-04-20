import requests
import json
from src.Hardware_Comms.ESPHTTPTopics import GetJSONVars, SetJSONVars, HTTPTopics
from src.Hardware_Comms.connectionData import ConnectionDataHandler
from src.Robot_Locomotion.MotorEnums import PWMVals
import threading

class WiFiComms:
    """
    communiation over wifi
    """

    # TODO make this static

    def __init__(self, shouldConnectToWiFi):
        """
        initializes wifi connection and IP
        :param shouldConnectToWiFi: [Bool] True if we want to connect to ESP, False otherwise
        """
        # esp32 IP
        self.IP = "http://192.168.49.241"
        # initialzies get vars
        self.getJson = {}
        for var in GetJSONVars:
            self.getJson[var.value] = PWMVals.STOPPED.value
        # initialize set vars
        self.setJson = {}
        for var in SetJSONVars:
            self.setJson[var.value] = PWMVals.STOPPED.value
        # not in PIDTuningState unless the state is entered through GUI
        # PID bool value set to 0 for false
        # self.setJson[SetJSONVars.PID.value] = 0
        self.setJson[SetJSONVars.TUNING_KP.value] = 0
        self.setJson[SetJSONVars.TUNING_KI.value] = 0
        self.setJson[SetJSONVars.TUNING_KD.value] = 0
        self.setJson[SetJSONVars.SETTING_HEADING.value] = 0
        # determine is ESP is connected
        # if not done here, all http requests take forever and it slows down program
        self.heading = 0
        if shouldConnectToWiFi:
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
        """
        does a get request for get json vars
        :param param: The topic to ask for
        :return: [String] the topic info
        """
        # print("Getting info of " + str(param))
        if not self.isConnected:
            return "No ESP Connected"
        # sending get request and saving the response as response object
        try:
            if param == "ESTOP":
                r = requests.get(url=self.IP + HTTPTopics.ESTOP.value)
                print("Robot has ESTOPPED")
                return "Robot has ESTOPPED"
            r = requests.get(url=self.IP + HTTPTopics.ROBOT_DATA.value)
            # TODO get the param
            info = json.loads(r.content.decode("utf-8"))
            if not param in info.keys():
                print(param + " not found in robot data.")
            return info[param]
        except:
            print("No connection could be established with ESP from getInfo")
            return "ESP Comms Err"

    def sendInfo(self, pairs):
        """
        sets values over wifi
        :param topic: the topic
        :param value: the value
        """
        for topic, value in pairs.items():
            self.setJson[topic] = value
            if not self.isConnected:
                print("asking ", value, " of ", topic)

        if not self.isConnected:
            return
        try:
            response = requests.post(self.IP + HTTPTopics.MAIN.value, json=self.setJson)
            self.parseResponse(response)
            self.connectionHandler.execute(response.elapsed.total_seconds())
        except Exception as e:
            print("No connection could be established with ESP from SendInfo")
            print(e)
            self.connectionHandler.loss()
            return "ESP Comms Err"

    def parseResponse(self, response):
        """
        given a response, parses the changed values and notifies observers of them
        :param response: the response to parse
        """
        pass
        #FOR DEBUG
        #print(response)
        # for item in response
        #   if diff from self.GetJSON
        #       change val in self.GETJSON
        #       notify observers

    def notifyObservers(self, topic, value):
        """
        notify observers of change
        :param topic: the topic
        :param value: the value
        """
        for observer in self.observers:
            observer.notify(topic, value)

    def attachObserver(self, observer):
        """
        attaches an observer
        :param observer: the observer
        """
        self.observers.append(observer)
