class ConnectionData:
    packetID = 0
    returnTime = 0

    def __init__(self):
        pass

    def execute(self, rtt):
        ## given an rtt, plot this on a graph?
        print(rtt)

    def calculateReturnTime(self):
        pass

    def calculatePacketLoss(self):
        pass

    def send(self):
        pass

    def received(self):
        pass
