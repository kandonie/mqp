from src.GUI.mainWindow import MainWindow
from PyQt5 import QtWidgets
import sys  # We need sys so that we can pass argv to QApplication
from src.GUI.RCGUI import RCGUI
from src.GUI.WindowEnums import WindowEnums


class GUIManager:
    """
    Creates and displays/hides various windows on appropriate events
    """

    def __init__(self, observers, wifi, robot):
        """
        initializes GUIs and shows main window
        :param observers: [Observers[]] the observers of the GUI_Manager
        :param observees: [Observees[]]the classes the GUI_Manager observes
        """

        # create main window
        app = QtWidgets.QApplication(sys.argv)
        self.main = MainWindow(wifi, robot)

        # attach observers
        observers.append(self)
        for observer in observers:
            self.attachObserver(observer)
        self.observers = observers
        self.rcgui = RCGUI(self.observers)

        # execute main window app
        self.main.show()

        sys.exit(app.exec_())

    def attachObserver(self, observer):
        """
        attaches observers to the main window
        :param observer: [Observer]: must have a notify function that takes 2 params.
        """
        self.main.attachObserver(observer)

    def notify(self, topic, value):
        """
        the function that should be called to notify this class of somethign
        :param topic: [any] the topic of the notification
        :param value: [any] the value of the notification
        """
        if topic == WindowEnums.RC:
            self.rcgui.show()
            self.main.hide()
        elif topic == WindowEnums.MAIN:
            self.main.show()
            self.main.setStateToIdle()
            self.rcgui.hide()
