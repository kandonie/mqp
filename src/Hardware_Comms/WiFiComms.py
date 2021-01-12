import requests
from src.Hardware_Comms.ESPHTTPTopics import GetJSONVars_T, SetJSONVars_T, HTTPTopics_T
from src.Hardware_Comms.connectionData import ConnectionDataHandler
from src.Robot_Locomotion.MotorEnums import PWMVals_T


class WiFiComms:
    """
    communiation over wifi
    """

    # TODO make this static

    def __init__(self, should_connect_to_wi_fi):
        """
        initializes wifi connection and IP
        :param should_connect_to_wi_fi: [Bool] True if we want to connect to ESP, False otherwise
        """
        # esp32 IP
        self.IP = "http://192.168.50.129"
        # initialzies get vars
        self.get_json = {}
        for var in GetJSONVars_T:
            self.get_json[var.value] = PWMVals_T.STOPPED.value
        # initialize set vars
        self.set_json = {}
        for var in SetJSONVars_T:
            self.set_json[var.value] = PWMVals_T.STOPPED.value
        # determine is ESP is connected
        # if not done here, all http requests take forever and it slows down program
        if should_connect_to_wi_fi == True:
            try:
                print("Trying to connect to ESP...")
                requests.post(self.IP + HTTPTopics_T.MAIN.value, json=self.set_json)
                self.is_connected = True
                print("done!")
            except:
                print("failed")
                self.is_connected = False
        else:
            self.is_connected = False
            self.heading = 0

        self.connection_handler = ConnectionDataHandler()
        self.observers = []

    def getInfo(self, param):
        """
        does a get request for get json vars
        :param param: The topic to ask for
        :return: [String] the topic info
        """
        # TODO Might want to delete this function
        print("Getting info of " + str(param))
        if not self.is_connected:
            return "No ESP Connected"
        # sending get request and saving the response as response object
        try:
            r = requests.get(url=self.IP + HTTPTopics_T.MAIN.value)
            # TODO get the param
            return r.content
        except:
            print("No connection could be established with ESP")
            return "ESP Comms Err"

    def sendInfo(self, topic, value):
        """
        sets values over wifi
        :param topic: the topic
        :param value: the value
        """
        print("asking " + str(value) + " of " + str(topic))
        if not self.is_connected:
            self.notifyObservers(GetJSONVars_T.HEADING, str(self.heading))
            #for testing purposes
            self.heading += 10
            self.heading %= 100
            return
        try:
            self.set_json[topic] = value
            response = requests.post(self.IP + HTTPTopics_T.MAIN.value, json=self.set_json)
            self.parseResponse(response)
            self.connection_handler.execute(response.elapsed.total_seconds())
        except:
            print("No connection could be established with ESP")
            self.connection_handler.loss()
            return "ESP Comms Err"

    def parseResponse(self, response):
        """
        given a response, parses the changed values and notifies observers of them
        :param response: the response to parse
        """
        print(response)
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
