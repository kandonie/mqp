from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow,
                             QComboBox, QLabel, QButtonGroup,
                             QHBoxLayout, QVBoxLayout, QLineEdit,
                             QRadioButton)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from Guidance.GuidanceEnums import IntelligenceStates, BehavioralStates
from Hardware_Comms.ESPHTTPTopics import SetJSONVars, GetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals
from GUI.WindowEnums import WindowEnums
from GUI.DataGraph import DataGraph


class MainWindow(QMainWindow):
    """
    This class contains a main window for the application.
    """

    def __init__(self, GUI_Graphs):
        """
        init initializes the QWidgets and sets the geometry of the window
        :param GUI_Graphs: [Bool] True to display graphs, False otherwise
        """
        super().__init__()

        self.hasGraphs = GUI_Graphs

        # make main window
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("Basic GUI")

        # important for setting locations of QWidgets
        self.observers = []

        self.initializeLayout()
        self.mainWidget.setLayout(self.layout)

        print("done GUI creation")

    def attachObserver(self, observer):
        """
        adds an of observers to its own list
        :param observer: [Observer] must have a notify function that takes 2 args.
        """
        self.observers.append(observer)

    def initializeLayout(self):
        """
        sets the locations of all widgets on the GUI
        """
        self.layout = QHBoxLayout(self.mainWidget)
        first_col = QVBoxLayout(self.mainWidget)

        # add widgets to first col
        self.makeESTOPButton(first_col)
        self.makeRobotSystemEnablingButtons(first_col)
        self.makeIntelligenceStateComboBox(first_col)
        self.makePWMButtons(first_col)
        self.makePolygonalMovement(first_col)
        self.makeSensorLabels(first_col)

        self.layout.addLayout(first_col)

        if self.hasGraphs:
            second_col = QVBoxLayout(self.mainWidget)
            self.makeGraphs(second_col)
            self.layout.addLayout(second_col)

    def makeESTOPButton(self, layout):
        """
        make the ESTOP button and add it to layout
        :param layout: the layout to add the ESTOP to
        """
        self.ESTOPButton = QPushButton(self.mainWidget)
        self.ESTOPButton.setText("Estop")
        self.ESTOPButton.clicked.connect(self.ESTOP)

        layout.addWidget(self.ESTOPButton)

    def ESTOP(self):
        """
        alerts observers that an ESTOP is requested
        """
        self.notifyObservers(BehavioralStates.ESTOP, "ESTOP")

    def makeRobotSystemEnablingButtons(self, layout):
        """
        makes the radio buttons that toggle drive enabled on/pff
        :param layout: the layout to add the radio buttons to
        """
        # dict of label to params for notifying of click (topic, value)
        self.enablingLabels = {}
        self.enablingLabels["Disable Drive"] = (SetJSONVars.DRIVE_ENABLE_CHANGE, "false")
        self.enablingLabels["Enable Drive"] = (SetJSONVars.DRIVE_ENABLE_CHANGE, "true")
        self.enablingLabels["Disable Weapon"] = (SetJSONVars.WEAPON_ENABLE_CHANGE, "false")
        self.enablingLabels["Enable Weapon"] = (SetJSONVars.WEAPON_ENABLE_CHANGE, "true")

        driveRadioHBox = QHBoxLayout(self.mainWidget)
        self.drive_enabled_group = QButtonGroup()
        weaponRadioHBox = QHBoxLayout(self.mainWidget)
        self.weapon_enabled_group = QButtonGroup()

        count = 0
        for label in self.enablingLabels.keys():
            button = self.makeRadioButton(label)
            if count < 2:
                driveRadioHBox.addWidget(button)
                self.drive_enabled_group.addButton(button)
            else:
                weaponRadioHBox.addWidget(button)
                self.weapon_enabled_group.addButton(button)
            if count % 2 == 0:
                button.setChecked(True)
            else:
                button.setChecked(False)
            count += 1

        layout.addLayout(driveRadioHBox)
        layout.addLayout(weaponRadioHBox)

    def makeRadioButton(self, label):
        """
        makes a radio button
        is in a function cuz python loop scope bad
        :param label: [String]
        :return: [QRadioButton] the button
        """
        button = QRadioButton(label, self.mainWidget)
        button.toggled.connect(lambda: self.enableChanged(button))
        return button

    def enableChanged(self, button):
        """
        callback for system enabled radio buttons (drive, weapon)
        :param arm_button: [QRadioButton] the button that's been changed
        """
        if button.isChecked():
            if button.text() in self.enablingLabels.keys():
                params = self.enablingLabels[button.text()]
                self.notifyObservers(params[0], params[1])

    def makeIntelligenceStateComboBox(self, layout):
        # make label
        label = QLabel(self.mainWidget)
        label.setText("Intelligence State")

        # make combobox
        # Is self because setToIdle needs it
        self.intelligenceStateComboBox = QComboBox(self.mainWidget)
        self.intelligenceStateComboBox.addItems(IntelligenceStates.list_states())
        self.intelligenceStateComboBox.activated[str].connect(self.intelligenceStateChanged)

        # followed by intelligence state combo box
        intelligenceHBox = QHBoxLayout(self.mainWidget)
        intelligenceHBox.addWidget(label)
        intelligenceHBox.addWidget(self.intelligenceStateComboBox)
        layout.addLayout(intelligenceHBox)

    def intelligenceStateChanged(self, text):
        """
        notfies observers of change in intelligence state
        :param text: [String] The new intelligence state (must correspond to an IntelligenceStateEnum)
        """
        state = None
        for s in IntelligenceStates:
            if text == s.value:
                state = s
                break
        self.notifyObservers(state, text)
        if state == IntelligenceStates.RC:
            self.notifyObservers(WindowEnums.RC, WindowEnums.RC.value)

    def makePWMButtons(self, layout):
        """
        creates all the push buttons
        """
        pwmLabel = QLabel(self.mainWidget)
        pwmLabel.setText("Individually set PWMs")
        layout.addWidget(pwmLabel)

        motors = [SetJSONVars.MOTOR1_PWM, SetJSONVars.WEAPON_PWM, SetJSONVars.MOTOR2_PWM]

        for motor in motors:
            hBox = self.makeMotor(motor)
            layout.addLayout(hBox)

    def makeMotor(self, motor):
        """
        makes GUI stuff for each motor
        Can't do in for loop because variable scope bad
        :param motor: the name of the motor
        :return: an hbox with the motor qlineedit and send button
        """
        qEditWidth = 100

        hBox = QHBoxLayout(self.mainWidget)
        validator = QIntValidator(int(PWMVals.FULL_CCW.value), int(PWMVals.FULL_CW.value))
        PWMInput = QLineEdit(PWMVals.STOPPED.value, self.mainWidget)
        PWMInput.setValidator(validator)
        PWMInput.setMaxLength(4)
        PWMInput.setFixedWidth(qEditWidth)
        hBox.addWidget(PWMInput)

        sendPWMButton = QPushButton(self.mainWidget)
        label = "Set PWM for " + motor.value
        sendPWMButton.setText(label)
        sendPWMButton.clicked.connect(lambda: self.sendPWM(PWMInput, motor))
        hBox.addWidget(sendPWMButton)

        return hBox

    def sendPWM(self, qLineEdit, motor):
        """
        alerts observers of change in pwm
        """
        val = int(qLineEdit.text())
        if val < int(PWMVals.FULL_CCW.value) or val > int(PWMVals.FULL_CW.value):
            print(
                "Not sending. Value not in range. Range is " + PWMVals.FULL_CCW.value
                + " to " + PWMVals.FULL_CW.value)
            return
        self.notifyObservers(BehavioralStates.PWM, (motor, qLineEdit.text()))

    def makePolygonalMovement(self, layout):
        label = QLabel(self.mainWidget)
        label.setText("Drive polygon, n sides")
        layout.addWidget(label)

        # callback needs this to be self
        hBox = QHBoxLayout(self.mainWidget)
        self.movementQLineEdit = QLineEdit("3", self.mainWidget)
        self.movementQLineEdit.setValidator(QIntValidator())
        self.movementQLineEdit.setMaxLength(1)
        hBox.addWidget(self.movementQLineEdit)

        button = QPushButton(self.mainWidget)
        button.setText("Send Movement Info")
        button.clicked.connect(self.sendMovement)
        hBox.addWidget(button)
        layout.addLayout(hBox)

    def sendMovement(self):
        """
        notifies observers of change in movement desired with desired value
        """
        value = self.movementQLineEdit.text()
        if not value:
            value = '0'
        elif int(value) < 3:
            print("Polygon needs at least 2 sides")
            return
        self.notifyObservers(BehavioralStates.MOVEMENT_TEST, int(value))

    def makeSensorLabels(self, layout):
        self.sensorLabels = {}
        for sensor in GetJSONVars:
            hbox = QHBoxLayout(self.mainWidget)

            label = QLabel(self.mainWidget)
            label.setFixedWidth(300)
            label.setText(sensor.value)
            hbox.addWidget(label)

            data = QLabel(self.mainWidget)
            data.setText("   0")
            hbox.addWidget(data)

            layout.addLayout(hbox)
            self.sensorLabels[sensor] = (label, data)

    def makeGraphs(self, layout):
        """
        makes all of the graphs
        """
        self.sensorGraphs = {}
        for sensor in GetJSONVars:
            self.sensorGraphs[sensor] = DataGraph(sensor.value, (-100, 100))
            layout.addWidget(self.sensorGraphs[sensor])

    def notify(self, topic, value):
        """
        get notified of
        :param topic: the topic
        :param value: the value
        """
        if topic in GetJSONVars:
            # update specific graph
            if self.hasGraphs:
                graph = self.sensorGraphs[topic]
                if value != graph.getCurrData():
                    graph.update_plot(value)

            # update label on GUI
            self.sensorLabels[topic][1].setText(value)

    def notifyObservers(self, topic, value):
        """
        notifies observers of topic with value
        :param topic:  a topic
        :param value: a value
        """
        for observer in self.observers:
            observer.notify(topic, value)

    def setStateToIdle(self):
        """
        sets the current state to IDLE
        """
        self.intelligenceStateChanged(IntelligenceStates.IDLE.value)
        index = self.intelligenceStateComboBox.findText(IntelligenceStates.IDLE.value, Qt.MatchFixedString)
        if index >= 0:
            self.intelligenceStateComboBox.setCurrentIndex(index)
