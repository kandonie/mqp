import sys
import threading
sys.path.insert(1, '~/mqp')
from Guidance.stateMachine import StateMachine
from GUI.guiDataManager import GUIDataManager
from Hardware_Comms.WiFiComms import WiFiComms


def main():
    #create a wifi object 
    #TODO might want to make wifi static
    wifi = WiFiComms()
    #create state machine
    sm = StateMachine(wifi)
    try:
        #state machine needs to be in own thread because the GUI will take up this thread
        thread = threading.Thread(target=sm.runStateMachine)
        thread.start()
    except:
        print("Couldn't start state machine")
    #start GUI (won't return until GUI window is closed )
    dm = GUIDataManager([sm])


if __name__ == "__main__":
    main()