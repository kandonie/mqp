class ConnectionDataHandler:

    def __init__(self):
        self.packetID = 0
        self.packetHistory = []
        self.historyLimit = 100
        self.lostPackets = 0
        self.packetLoss = 0

    def execute(self, rtt):
        """
        add the packet's rtt to packetHistory and call other handlers
        :param rtt: [int]   the round trip time of the latest successful packet
        """
        if len(self.packetHistory) >= self.historyLimit:
            self.packetHistory.pop(0)
        self.packetHistory.append(rtt)
        ConnectionDataHandler.handleReturnTime(rtt)
        self.packetLoss = ConnectionDataHandler.calculatePacketLoss(self.packetHistory, self.lostPackets)

    @staticmethod
    def handleReturnTime(rtt):
        """
        print the return time
        #TODO make a graph to plot the return time
        :param rtt: [int]   the round trip time of a packet
        :return:
        """
        print("rtt: " + str(rtt))

    @staticmethod
    def calculatePacketLoss(packetHistory, lost):
        """
        calculate the percentage of packets lost over a set history of packets
        :param packetHistory:   [[int]]     a list of packet rtt's for a recent history of packets
        :param lost:            [int]       the number of packets sent that did not go through
        :return:                [int]       the packet loss percentage, in decimal
        """
        received = len(packetHistory)
        return lost / received

    def loss(self):
        self.lostPackets += 1
