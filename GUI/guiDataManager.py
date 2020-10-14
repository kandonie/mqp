from Guidance.observer import Observer
from GUI.viewManager import ViewManager
from GUI.graphGui import MainWindow
from PyQt5 import QtWidgets
import sys  # We need sys so that we can pass argv to QApplication
import os

class GUIDataManager:
    def __init__(self):
        self.cameraImage = None
        self.viewManager = ViewManager()
        self.buttons = []
        self.attribute = None


        app = QtWidgets.QApplication(sys.argv)
        main = MainWindow()
        main.show()
        sys.exit(app.exec_())
