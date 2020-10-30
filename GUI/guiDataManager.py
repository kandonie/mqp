from GUI.basicGUI import MainWindow
from PyQt5 import QtWidgets
import sys  # We need sys so that we can pass argv to QApplication

class GUIDataManager:
    def __init__(self, observers):
        self.cameraImage = None
        self.buttons = []
        self.attribute = None

        app = QtWidgets.QApplication(sys.argv)
        self.main = MainWindow()
        for observer in observers:
            self.attachObserver(observer)
        self.main.show()
        sys.exit(app.exec_())

    def attachObserver(self, observer):
        print("attaching")
        self.main.attachObserver(observer)