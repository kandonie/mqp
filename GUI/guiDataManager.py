from GUI.basicGUI import MainWindow
from PyQt5 import QtWidgets
import sys  # We need sys so that we can pass argv to QApplication

class GUIDataManager:
    """Displays a main window
    """
    def __init__(self, observers):
        """initializes variables and shows main window

        Args:
            observers ([observers]): a list of observers to be notified of GUI events.
        """

        #create main window
        app = QtWidgets.QApplication(sys.argv)
        self.main = MainWindow()

        #attach observers
        for observer in observers:
            self.attachObserver(observer)

        #execute main window app
        self.main.show()
        sys.exit(app.exec_())

    def attachObserver(self, observer):
        """attaches observers to the main window

        Args:
            observer (Observer): must have a notify function that takes 2 params. 
        """        
        self.main.attachObserver(observer)

    def notify(self, topic, value, *args):
        pass
