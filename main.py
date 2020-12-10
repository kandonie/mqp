import sys
import threading
sys.path.insert(1, '~/mqp')
from Guidance.stateMachine import StateMachine
from GUI.GUIManager import GUIManager
from Hardware_Comms.WiFiComms import WiFiComms
from Sensing.cv import CV
from Sensing.imu import IMU
from Sensing.motorCurrent import MotorCurrent


def main(connectToWiFi):
    #create a wifi object 
    #TODO might want to make wifi static
    wifi = WiFiComms(connectToWiFi)
    #create state machine
    sm = StateMachine(wifi)
    wifi.attachObserver(sm)
    try:
        #state machine needs to be in own thread because the GUI will take up this thread
        thread = threading.Thread(target=sm.runStateMachine)
        thread.daemon = True
        thread.start()
    except:
        print("Couldn't start state machine")

    #start GUI (won't return until GUI window is closed )
    GUIManager([sm], [wifi])###ANYTHING WRITTEN PAST THIS LINE WILL NOT BE RUN until app closes
    sys.exit()
    #TODO these lines were never run before and are now erroring.
    #TODO fix the errors, they didn't run previously because the GUIDataManager
    #line used to loop
    #imu = IMU()
    #imu.attachObservers([sm, dm])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "True":
            main(True)
        else:
            main(False)
    else:
        main(True)
