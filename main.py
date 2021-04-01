import sys
import threading

sys.path.insert(1, '~/mqp')
from src.Guidance.stateMachine import StateMachine
from src.GUI.GUIManager import GUIManager
from src.Hardware_Comms.WiFiComms import WiFiComms
from src.Sensing.RobotDataManager import RobotDataManager
from src.CV.stickerDetect import StickerDetector
from src.CV.arucoDetect import ArucoDetector
from src.Robot_Locomotion.drive import Drive
from src.Robot_Locomotion.weapon import Weapon
from src.Robot_Locomotion.robot import Robot


def main(connectToWiFi):
    """
    runs the main program
    :param connectToWiFi: True if we should connect to wifi, false otherwise
    """
    # create a wifi object
    wifi = WiFiComms(connectToWiFi)
    robotDataManager = RobotDataManager()
    drive = Drive(wifi)
    weapon = Weapon(wifi)
    robot = Robot(wifi, drive, weapon)
    # create the CV model
    cv = ArucoDetector([robotDataManager, robot])
    # create state machine
    sm = StateMachine(wifi, robot, drive, weapon)
    wifi.attachObserver(robotDataManager)


    try:
        # state machine needs to be in own thread because the GUI will take up this thread
        thread = threading.Thread(target=sm.runStateMachine)
        thread.daemon = True
        thread.start()
    except:
        print("Couldn't start state machine")

    try:
        # cv model needs to be in own thread because the GUI will take up this thread
        cv_thread = threading.Thread(target=cv.runModel)
        cv_thread.daemon = True
        cv_thread.start()
    except:
        print("Couldn't start CV model")

    # start GUI (won't return until GUI window is closed )
    GUIManager([sm], wifi, robot)  ###ANYTHING WRITTEN PAST THIS LINE WILL NOT BE RUN until app closes
    sys.exit()


if __name__ == "__main__":
    """
    parses the command line input and calls main
    """
    connectToWiFi = True
    # Connect to wifi option
    if len(sys.argv) >= 1:
        if sys.argv[1] != "True":
            connectToWiFi = False
    main(connectToWiFi)
