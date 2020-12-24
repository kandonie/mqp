import sys
import threading

sys.path.insert(1, '~/mqp')
from src.Guidance.stateMachine import StateMachine
from src.GUI.GUIManager import GUIManager
from src.Hardware_Comms.WiFiComms import WiFiComms
from src.Sensing.RobotDataManager import RobotDataManager


def main(connectToWiFi, GUI_Graphs):
    """
    runs the main program
    :param connectToWiFi: True if we should connect to wifi, false otherwise
    :param GUI_Graphs: True if graphs should be displayed, false otherwise
    """
    # create a wifi object
    wifi = WiFiComms(connectToWiFi)
    # create state machine
    robotDataManager = RobotDataManager()
    sm = StateMachine(wifi)
    wifi.attachObserver(robotDataManager)


    try:
        # state machine needs to be in own thread because the GUI will take up this thread
        thread = threading.Thread(target=sm.runStateMachine)
        thread.daemon = True
        thread.start()
    except:
        print("Couldn't start state machine")

    # start GUI (won't return until GUI window is closed )
    GUIManager([sm], [], GUI_Graphs)  ###ANYTHING WRITTEN PAST THIS LINE WILL NOT BE RUN until app closes
    sys.exit()


if __name__ == "__main__":
    """
    parses the command line input and calls main
    """
    connectToWiFi = True
    GUI_Graphs = True
    # Connect to wifi option
    if len(sys.argv) > 1:
        if sys.argv[1] != "True":
            connectToWiFi = False
    # have graphs option
    if len(sys.argv) > 2:
        if sys.argv[2] != "True":
            GUI_Graphs = False
    main(connectToWiFi, GUI_Graphs)
