import sys
sys.path.insert(1, '~/mqp')
from Guidance.stateMachine import StateMachine
from GUI.guiDataManager import GUIDataManager
def main():
    sm = StateMachine()
    print("I made a state machine")
    dm = GUIDataManager()
    print("I made and closed a GUI")


if __name__ == "__main__":
    main()