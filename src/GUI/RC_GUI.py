from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QSlider
from src.GUI.WindowEnums_T import WindowEnums_T
from PyQt5.Qt import Qt
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeyEvent
from src.Guidance.GuidanceEnums import BehavioralStates_T
from src.Robot_Locomotion.MotorEnums import PWMVals_T

class MyDumbSlider(QSlider):
    """
    basically bad things were happening iwth key pressed
    events not being heard for RCGUI when this did stuff,
    SO Here we are doing this so that we can still have keyboard commands
    """
    def __init__(self, horizontal, parent):
        super(MyDumbSlider, self).__init__(horizontal, parent)

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        #intentionally do nothing
        pass

    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        #intentionally do nothing
        pass



class RC_GUI(QMainWindow):
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
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("RC GUI")

        # important for setting locations of QWidgets
        self.observers = observers

        self.initializeLayout()
        self.main_widget.setLayout(self.layout)
        print("done RC GUI creation")

    def initializeLayout(self):
        self.layout = QHBoxLayout(self.main_widget)

        first_col = QVBoxLayout(self.main_widget)
        self.makeInstructions(first_col)
        self.makeSpeedOption(first_col)

        self.layout.addLayout(first_col)

    def makeInstructions(self, layout):
        """
        makes the label that displays the RC instructions on the GUI
        """
        instructions_label = QLabel(self.main_widget)
        text = "Space bar for ESTOP\n"
        text += "Up arrow key for drive forward\nDown arrow key for drive backward\n"
        text += "Right arrow key for rotate CW\nLeft arrow key for rotate CCW\n"
        text += "'w' key for toggle weapon on/off\n'/' key for stop drive motors\n"
        text += "close this window to return to the main window\n"
        instructions_label.setText(text)
        layout.addWidget(instructions_label)

    def makeSpeedOption(self, layout):
        max_pwm_diff = int(PWMVals_T.FULL_CW.value) - int(PWMVals_T.STOPPED.value)
        label = QLabel(self.main_widget)
        label.setText("Motor speed (PWM Diff from 0 for each motor, 0-" + str(max_pwm_diff) + ")")
        layout.addWidget(label)

        h_box = QHBoxLayout(self.main_widget)
        self.slider = MyDumbSlider(Qt.Horizontal, self.main_widget)
        self.slider.setMinimum(0)
        self.slider.setMaximum(max_pwm_diff)
        self.slider.valueChanged.connect(self.sliderValChanged)
        self.slider.installEventFilter(self)
        h_box.addWidget(self.slider)

        self.slider_label = QLabel(self.main_widget)
        self.slider_label.setText("0")
        h_box.addWidget(self.slider_label)

        layout.addLayout(h_box)

    def sliderValChanged(self, val):
        self.slider_label.setText(str(val))

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            source is self.slider):
            self.keyPressEvent(event)
        elif (event.type() == QEvent.KeyRelease and
            source is self.slider):
            self.keyReleaseEvent(event)
        return super(RC_GUI, self).eventFilter(source, event)

    def keyPressEvent(self, event):
        """
        when a key is pressed, notify the observers
        :param event: a key press
        """
        self.notifyObservers(BehavioralStates_T.RC, (event.key(), self.slider.value()))

    def keyReleaseEvent(self, event):
        """
        notify the observers of the key released
        :param event: the key released
        """
        # The autorepeat debounces
        if not event.isAutoRepeat():
            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down or (
                    event.key() == Qt.Key_Left) or event.key() == Qt.Key_Right:
                self.notifyObservers(BehavioralStates_T.RC, (Qt.Key_Slash, "0"))
            # this is so the next time we press w we know it's a new key
            elif event.key() == Qt.Key_W:
                self.notifyObservers(BehavioralStates_T.RC, (Qt.Key_Q, "0"))

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
        self.notifyObservers(WindowEnums_T.MAIN, WindowEnums_T.MAIN.value)

    def notifyObservers(self, topic, value):
        """
        notifies observers of topic with value
        :param topic: the topic
        :param value: the value
        """
        for observer in self.observers:
            observer.notify(topic, value)
