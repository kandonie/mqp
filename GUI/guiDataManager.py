from GUI.mainWindow import MainWindow
from PyQt5 import QtWidgets
import sys  # We need sys so that we can pass argv to QApplication
from GUI.RCGUI import RCGUI
from GUI.WindowEnums import WindowEnums

class GUIDataManager:
    """Displays a main window
    """
    def __init__(self, observers, observees):
        """initializes variables and shows main window

        Args:
            observers ([observers]): a list of observers to be notified of GUI events.
        """

        #create main window
        app = QtWidgets.QApplication(sys.argv)
        self.main = MainWindow()

        #attach observers
        observers.append(self)
        for observer in observers:
            self.attachObserver(observer)
        self.observers = observers
        
        for observee in observees:
            observee.attachObserver(self.main)

        #execute main window app
        self.main.show()
        self.rcgui = RCGUI(self.observers)
        
        sys.exit(app.exec_())

    def attachObserver(self, observer):
        """attaches observers to the main window

        Args:
            observer (Observer): must have a notify function that takes 2 params. 
        """        
        self.main.attachObserver(observer)


    def notify(self, topic, value):
        if topic == WindowEnums.RC:
            self.rcgui.show()
            self.main.hide()
        elif topic == WindowEnums.MAIN:
            self.main.show()
            self.main.setStateToIdle()
            self.rcgui.hide()
        pass
