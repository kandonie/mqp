from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QButtonGroup, QLineEdit, QRadioButton
from GUI.WindowEnums import WindowEnums
from PyQt5.Qt import Qt
from Guidance.GuidanceEnums import BehavioralStates

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

        self.makeInstructions()

        self.setWidgetLocations()
        print("done RC GUI creation")

    def makeInstructions(self):
        self.instructionsLabel = QLabel(self.mainWidget)
        text = "Space bar for ESTOP\n"
        text += "Up arrow key for drive forward\nDown arrow key for drive backward\n"
        text += "Right arrow key for rotate CW\nLeft arrow key for rotate CCW\n"
        text += "'w' key for toggle weapon on/off\n'/' key for stop drive motors\n"
        text += "close this window to return to the main window\n"
        self.instructionsLabel.setText(text)


    def setWidgetLocations(self):
        start_x = 50
        start_y = 50
        widgetSpacing = 20 #num pixels between widgets
        sectionSpacing = 60
        #TODO make spacing good and consistent
        instruccionsY = start_y
        self.instructionsLabel.move(start_x, instruccionsY )


        self.setGeometry(500, start_y, 1000, 1000)


    def keyPressEvent(self, event):
        self.notifyObservers(BehavioralStates.RC, event.key())


    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat() and ( event.key() == Qt.Key_Up or event.key() == Qt.Key_Down or event.key() == Qt.Key_Left or event.key() == Qt.Key_Right):
            self.notifyObservers(BehavioralStates.RC, Qt.Key_Slash)


    def closeEvent(self, event):
        event.accept() # let the window close
        self.returnHome()


    def returnHome(self):
        """
        open basicGUI window
        """
        self.notifyObservers(WindowEnums.MAIN, WindowEnums.MAIN.value)
        pass


    def notifyObservers(self, topic, value, *args):
        """notifies observers of topic with value

        Args:
            topic (CommsTopics): a communication topic
            value (string): the value for the comm topic
        """
        for observer in self.observers:
            observer.notify(topic, value)
