from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QSlider
from GUI.WindowEnums import WindowEnums
from PyQt5.Qt import Qt
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeyEvent
from Guidance.GuidanceEnums import BehavioralStates
from Robot_Locomotion.MotorEnums import PWMVals

class myDumbSlider(QSlider):
    """
    basically bad things were happening iwth key pressed
    events not being heard for RCGUI when this did stuff,
    SO Here we are doing this so that we can still have keyboard commands
    """
    def __init__(self, horizontal, parent):
        super(myDumbSlider, self).__init__(horizontal, parent)

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        pass

    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        pass



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

        self.initializeLayout()
        self.mainWidget.setLayout(self.layout)
        print("done RC GUI creation")

    def initializeLayout(self):
        self.layout = QHBoxLayout(self.mainWidget)

        first_col = QVBoxLayout(self.mainWidget)
        self.makeInstructions(first_col)
        self.makeSpeedOption(first_col)

        self.layout.addLayout(first_col)

    def makeInstructions(self, layout):
        """
        makes the label that displays the RC instructions on the GUI
        """
        instructionsLabel = QLabel(self.mainWidget)
        text = "Space bar for ESTOP\n"
        text += "Up arrow key for drive forward\nDown arrow key for drive backward\n"
        text += "Right arrow key for rotate CW\nLeft arrow key for rotate CCW\n"
        text += "'w' key for toggle weapon on/off\n'/' key for stop drive motors\n"
        text += "close this window to return to the main window\n"
        instructionsLabel.setText(text)
        layout.addWidget(instructionsLabel)

    def makeSpeedOption(self, layout):
        maxPWMDiff = int(PWMVals.FULL_CW.value) - int(PWMVals.STOPPED.value)
        label = QLabel(self.mainWidget)
        label.setText("Motor speed (PWM Diff from 0 for each motor, 0-" + str(maxPWMDiff) + ")")
        layout.addWidget(label)

        hbox = QHBoxLayout(self.mainWidget)
        self.slider = myDumbSlider(Qt.Horizontal, self.mainWidget)
        self.slider.setMinimum(0)
        self.slider.setMaximum(maxPWMDiff)
        self.slider.valueChanged.connect(self.sliderValChanged)
        self.slider.installEventFilter(self)
        hbox.addWidget(self.slider)

        self.sliderLabel = QLabel(self.mainWidget)
        self.sliderLabel.setText("0")
        hbox.addWidget(self.sliderLabel)

        layout.addLayout(hbox)

    def sliderValChanged(self, val):
        self.sliderLabel.setText(str(val))

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            source is self.slider):
            self.keyPressEvent(event)
        elif (event.type() == QEvent.KeyRelease and
            source is self.slider):
            self.keyReleaseEvent(event)
        return super(RCGUI, self).eventFilter(source, event)

    def keyPressEvent(self, event):
        """
        when a key is pressed, notify the observers
        :param event: a key press
        """
        self.notifyObservers(BehavioralStates.RC, (event.key(), self.slider.value()))

    def keyReleaseEvent(self, event):
        """
        notify the observers of the key released
        :param event: the key released
        """
        # The autorepeat debounces
        if not event.isAutoRepeat():
            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down or (
                    event.key() == Qt.Key_Left) or event.key() == Qt.Key_Right:
                self.notifyObservers(BehavioralStates.RC, (Qt.Key_Slash, "0"))
            # this is so the next time we press w we know it's a new key
            elif event.key() == Qt.Key_W:
                self.notifyObservers(BehavioralStates.RC, (Qt.Key_Q, "0"))

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
