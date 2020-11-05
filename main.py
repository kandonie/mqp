import sys
import threading
sys.path.insert(1, '~/mqp')
from Guidance.stateMachine import StateMachine
from GUI.guiDataManager import GUIDataManager
from Hardware_Comms.WiFiComms import WiFiComms
def main():
    wifi = WiFiComms()
    sm = StateMachine(wifi)
    try:
        thread = threading.Thread(target=sm.runStateMachine)
        thread.start()
    except:
        print("Couldn't start state machine")
    dm = GUIDataManager([sm])


if __name__ == "__main__":
    main()