from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QButtonGroup, QLineEdit, QRadioButton
from PyQt5.QtGui import QIntValidator
from Guidance.GuidanceEnums import IntelligenceStates, BehavioralStates
from Hardware_Comms.ESPHTTPTopics import SetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals

class RCGUI(QMainWindow):

    """This class contains a main window for the application.
        This is a basic GUI which has simple features.

    Args:
        QMainWindow: This is of type QMainWindow
    """
    def __init__(self, observers):
        """init initializes the QWidgets and sets the geometry of the window
        """
        super().__init__()
        #make main window
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("RC GUI")

        #important for setting locations of QWidgets
        self.observers = observers

        self.setWidgetLocations()
        print("done RC GUI creation")


    def setWidgetLocations(self):
        start_x = 50
        start_y = 50
        widgetSpacing = 20 #num pixels between widgets
        sectionSpacing = 60
        #TODO make spacing good and consistent
        #Estop button
        # estop_y = start_y
        # self.ESTOPButton.move(start_x, estop_y)

        self.setGeometry(start_x, start_y, 1000, 1000)


    def notifyObservers(self, topic, value, *args):
        """notifies observers of topic with value

        Args:
            topic (CommsTopics): a communication topic
            value (string): the value for the comm topic
        """
        for observer in self.observers:
            observer.notify(topic, value)
