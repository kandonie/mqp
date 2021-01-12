class ConnectionDataHandler:
    # TODO Comment this @Kristen
    def __init__(self):
        self.packet_id = 0
        self.packet_history = []
        self.history_limit = 100
        self.lost_packets = 0
        self.packet_loss = 0

    def execute(self, rtt):
        """
        add the packet's rtt to packetHistory and call other handlers
        :param rtt: [int]   the round trip time of the latest successful packet
        """
        if len(self.packet_history) >= self.history_limit:
            self.packet_history.pop(0)
        self.packet_history.append(rtt)
        ConnectionDataHandler.handleReturnTime(rtt)
        self.packet_loss = ConnectionDataHandler.calculatePacketLoss(self.packet_history, self.lost_packets)

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
    def calculatePacketLoss(packet_history, lost):
        """
        calculate the percentage of packets lost over a set history of packets
        :param packet_history:   [[int]]     a list of packet rtt's for a recent history of packets
        :param lost:            [int]       the number of packets sent that did not go through
        :return:                [int]       the packet loss percentage, in decimal
        """
        received = len(packet_history)
        return lost / received

    def loss(self):
        self.lost_packets += 1
