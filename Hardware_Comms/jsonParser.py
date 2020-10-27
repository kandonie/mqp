import requests

class JSONParser:
    sensors = []

    def decodeJSON(self, sensorData):
        pass

    def encodeJSON(self, motorData):
        pass


# esp32 IP
IP = "http://192.168.4.1"
# sending get request and saving the response as response object
r = requests.get(url = IP + "/readAPOS")
print(r.content)
