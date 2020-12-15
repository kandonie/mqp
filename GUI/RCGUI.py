from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QButtonGroup, QLineEdit, QRadioButton
from GUI.WindowEnums import WindowEnums
from PyQt5.Qt import Qt
from Guidance.GuidanceEnums import BehavioralStates


class RCGUI(QMainWindow):
    """
    This class contains a window for the RC mode.
    """

    def __init__(self, observers):
        """
        init initializes the QWidgets and sets the geometry of the window
        :param observers: the classes that observe this GUI
        """
        super().__init__()
        # make main window
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("RC GUI")

        # important for setting locations of QWidgets
        self.observers = observers

        self.makeInstructions()

        self.setWidgetLocations()
        print("done RC GUI creation")

    def makeInstructions(self):
        """
        makes the label that displays the RC instructions on the GUI
        """
        self.instructionsLabel = QLabel(self.mainWidget)
        text = "Space bar for ESTOP\n"
        text += "Up arrow key for drive forward\nDown arrow key for drive backward\n"
        text += "Right arrow key for rotate CW\nLeft arrow key for rotate CCW\n"
        text += "'w' key for toggle weapon on/off\n'/' key for stop drive motors\n"
        text += "close this window to return to the main window\n"
        self.instructionsLabel.setText(text)

    def setWidgetLocations(self):
        """
        sets the locations of the widgets
        """
        start_x = 50
        start_y = 50
        widgetSpacing = 20  # num pixels between widgets
        sectionSpacing = 60
        instruccionsY = start_y
        self.instructionsLabel.move(start_x, instruccionsY)

        self.setGeometry(500, start_y, 1000, 1000)

    def keyPressEvent(self, event):
        """
        when a key is pressed, notify the observers
        :param event: a key press
        """
        self.notifyObservers(BehavioralStates.RC, event.key())

    def keyReleaseEvent(self, event):
        """
        notify the observers of the key released
        :param event: the key released
        """
        # The autorepeat debounces
        if not event.isAutoRepeat() and (
                event.key() == Qt.Key_Up
                or event.key() == Qt.Key_Down
                or event.key() == Qt.Key_Left
                or event.key() == Qt.Key_Right):
            self.notifyObservers(BehavioralStates.RC, Qt.Key_Slash)

    def closeEvent(self, event):
        """
        when the window closes, exit
        :param event: the window closing event
        """
        event.accept()  # let the window close
        self.returnHome()

    def returnHome(self):
        """
        open basicGUI window
        """
        self.notifyObservers(WindowEnums.MAIN, WindowEnums.MAIN.value)

    def notifyObservers(self, topic, value):
        """
        notifies observers of topic with value
        :param topic: the topic
        :param value: the value
        """
        for observer in self.observers:
            observer.notify(topic, value)
