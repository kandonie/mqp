from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow,
                             QComboBox, QLabel, QButtonGroup,
                             QHBoxLayout, QVBoxLayout, QLineEdit,
                             QRadioButton)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, QTimer
from src.Guidance.GuidanceEnums import IntelligenceStates, BehavioralStates
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars, GetJSONVars, RobotMovementType
from src.Robot_Locomotion.MotorEnums import PWMVals, PIDVals, MovementVals
from src.GUI.WindowEnums import WindowEnums
from src.GUI.DataGraph import DataGraph
from src.Sensing.RobotDataManager import RobotDataManager


class MainWindow(QMainWindow):
    """
    This class contains a main window for the application.
    """

    def __init__(self, GUI_Graphs, wifi):
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

        self.wifi = wifi

        # for dynamically updating sensor labels
        self.sensor_label = QLabel(self.mainWidget)
        self.sensor_data = QLabel(self.mainWidget)

        self.initializeLayout()
        self.mainWidget.setLayout(self.layout)

        RobotDataManager.getInstance().attachObserver(self)

    def attachObserver(self, observer):
        """
        adds an of observers to its own list
        :param observer: [Observer] must have a notify function that takes 2 args.
        """
        self.observers.append(observer)

    def reset(self):
        self.setStateToIdle()
        self.drive_enabled_group.buttons()[0].setChecked(True)
        self.weapon_enabled_group.buttons()[0].setChecked(True)
        for label in self.sensorLabels.values():
            label[1].setText("0")

    def initializeLayout(self):
        """
        sets the locations of all widgets on the GUI
        """
        self.layout = QHBoxLayout(self.mainWidget)
        first_col = QVBoxLayout(self.mainWidget)
        self.first_col = first_col

        # add widgets to first col
        self.makeESTOPButton(first_col)
        self.makeRobotSystemEnablingButtons(first_col)
        self.makeIntelligenceStateComboBox(first_col)
        self.makePWMButtons(first_col)
        self.makePIDButtons(first_col)
        self.makeHeadingButton(first_col)
        # self.makePolygonalMovement(first_col)
        self.makeSensorLabels(first_col)
        self.robotMovementTypeComboBox(first_col)

        # timer for sensor labels to send get requests periodically
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.updateSensorLabels)
        self.my_timer.start(10) # interval between get requests

        self.layout.addLayout(first_col)

        if self.hasGraphs:
            second_col = QVBoxLayout(self.mainWidget)
            self.makeGraphs(second_col)
            self.layout.addLayout(second_col)

        thirdCol = QVBoxLayout(self.mainWidget)
        self.makeBeginMatchButton(thirdCol)
        self.makeEndMatchButton(thirdCol)
        self.makeResetButton(thirdCol)
        self.layout.addLayout(thirdCol)

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
        # For testing
        self.enablingButtons = []

        self.enablingLabels = {}
        self.enablingLabels["Disable Drive"] = (
            SetJSONVars.DRIVE_ENABLE_CHANGE, "false")
        self.enablingLabels["Enable Drive"] = (
            SetJSONVars.DRIVE_ENABLE_CHANGE, "true")
        self.enablingLabels["Disable Weapon"] = (
            SetJSONVars.WEAPON_ENABLE_CHANGE, "false")
        self.enablingLabels["Enable Weapon"] = (
            SetJSONVars.WEAPON_ENABLE_CHANGE, "true")

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
        self.enablingButtons.append(button)
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
        self.intelligenceStateComboBox.addItems(
            IntelligenceStates.list_states())
        self.intelligenceStateComboBox.activated[str].connect(
            self.intelligenceStateChanged)

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
        self.motors = []
        pwmLabel = QLabel(self.mainWidget)
        pwmLabel.setText("Individually set PWMs")
        layout.addWidget(pwmLabel)

        motors = [SetJSONVars.MOTOR1_PWM,
                  SetJSONVars.MOTOR2_PWM, SetJSONVars.WEAPON_PWM]

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
        validator = QIntValidator(
            int(PWMVals.FULL_CCW.value), int(PWMVals.FULL_CW.value))
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
        self.motors.append((PWMInput, sendPWMButton, motor))
        return hBox

    def sendPWM(self, qLineEdit, motor_button):
        """
        alerts observers of change in pwm
        """
        val = int(qLineEdit.text())
        if val < int(PWMVals.FULL_CCW.value) or val > int(PWMVals.FULL_CW.value):
            print(
                "Not sending. Value not in range. Range is " + PWMVals.FULL_CCW.value
                + " to " + PWMVals.FULL_CW.value)
            if val < int(PWMVals.FULL_CCW.value):
                val = int(PWMVals.FULL_CCW.value)
            else:
                val = int(PWMVals.FULL_CW.value)
        self.notifyObservers(BehavioralStates.PWM, (motor_button, qLineEdit.text()))


    def makePIDButtons(self, layout):
        """
        creates all the push buttons
        """
        self.pid_gains = []
        pidLabel = QLabel(self.mainWidget)
        pidLabel.setText("Individually set PIDs")
        layout.addWidget(pidLabel)

        pid_gains = [SetJSONVars.KP,
                    SetJSONVars.KI, SetJSONVars.KD]

        for gain in pid_gains:
            hBox = self.makePIDGain(gain)
            layout.addLayout(hBox)

    def makePIDGain(self, gain):
        """
        makes GUI stuff for each pid gain
        Can't do in for loop because variable scope bad
        :param gain: the name of the pid gain
        :return: an hbox with the motor qlineedit and send button
        """
        qEditWidth = 100

        hBox = QHBoxLayout(self.mainWidget)
        PIDInput = QLineEdit(PIDVals.KP_DEFAULT.value, self.mainWidget)
        PIDInput.setFixedWidth(qEditWidth)
        hBox.addWidget(PIDInput)

        sendPIDButton = QPushButton(self.mainWidget)
        label = "Set PID for " + gain.value
        sendPIDButton.setText(label)
        sendPIDButton.clicked.connect(lambda: self.sendPID(PIDInput, gain))
        hBox.addWidget(sendPIDButton)
        self.pid_gains.append((PIDInput, sendPIDButton, gain))
        return hBox

    def sendPID(self, qLineEdit, gain_button):
        """
        alerts observers of change in pid
        """
        val = float(qLineEdit.text())
        self.notifyObservers(BehavioralStates.PID, (gain_button, qLineEdit.text()))

    def makeHeadingButton(self, layout):
        """
        creates all the push buttons
        """
        self.heading = []
        pidLabel = QLabel(self.mainWidget)
        pidLabel.setText("Individually set PIDs")
        layout.addWidget(pidLabel)

        heading = SetJSONVars.DESIRED_HEADING

        hBox = self.makeHeading(heading)
        layout.addLayout(hBox)

    def makeHeading(self, heading):
        """
        makes GUI stuff for each pid gain
        Can't do in for loop because variable scope bad
        :param gain: the name of the pid gain
        :return: an hbox with the motor qlineedit and send button
        """
        qEditWidth = 100

        hBox = QHBoxLayout(self.mainWidget)
        HeadingInput = QLineEdit(MovementVals.HEADING_DEFAULT.value, self.mainWidget)
        HeadingInput.setFixedWidth(qEditWidth)
        hBox.addWidget(HeadingInput)

        sendHeadingButton = QPushButton(self.mainWidget)
        label = "Set heading for " + heading.value
        sendHeadingButton.setText(label)
        sendHeadingButton.clicked.connect(lambda: self.sendHeading(HeadingInput, heading))
        hBox.addWidget(sendHeadingButton)
        self.heading.append((HeadingInput, sendHeadingButton, heading))
        return hBox

    def sendHeading(self, qLineEdit, heading_button):
        """
        alerts observers of change in pid
        """
        val = float(qLineEdit.text())
        self.notifyObservers(BehavioralStates.SET_HEADING, (heading_button, qLineEdit.text()))


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

        self.movementButton = QPushButton(self.mainWidget)
        self.movementButton.setText("Send Movement Info")
        self.movementButton.clicked.connect(self.sendMovement)
        hBox.addWidget(self.movementButton)
        layout.addLayout(hBox)

    def sendMovement(self):
        """
        notifies observers of change in movement desired with desired value
        """
        value = self.movementQLineEdit.text()
        if not value or int(value) < 3:
            print("Polygon needs at least 2 sides")
            return
        self.notifyObservers(BehavioralStates.MOVEMENT_TEST, int(value))

    def makeSensorLabels(self, layout):
        self.sensorLabels = {}
        for sensor in GetJSONVars:
            hbox = QHBoxLayout(self.mainWidget)

            self.sensor_label = QLabel(self.mainWidget)
            self.sensor_label.setFixedWidth(300)
            self.sensor_label.setText(sensor.value)
            hbox.addWidget(self.sensor_label)

            self.sensor_data = QLabel(self.mainWidget)
            data_val = str(self.wifi.getInfo(sensor.value))
            self.sensor_data.setText(data_val)
            hbox.addWidget(self.sensor_data)

            layout.addLayout(hbox)
            self.sensorLabels[sensor] = (self.sensor_label, self.sensor_data)

    # this updates the sensor labels on a periodic timer
    def updateSensorLabels(self):
        for sensor in GetJSONVars:
            data_val = str(self.wifi.getInfo(sensor.value))
            self.sensorLabels[sensor][1].setText(data_val)

    def robotMovementTypeComboBox(self, layout):
        # make label
        label = QLabel(self.mainWidget)
        label.setText("Robot Movement State")

        # make combobox
        # Is self because setToIdle needs it
        robotMovementStateComboBox = QComboBox(self.mainWidget)
        robotMovementStateComboBox.addItems(
            RobotMovementType.list_states())
        robotMovementStateComboBox.activated[str].connect(
            self.robotMovementChanged)

        # followed by intelligence state combo box
        robotMovementHBox = QHBoxLayout(self.mainWidget)
        robotMovementHBox.addWidget(label)
        robotMovementHBox.addWidget(robotMovementStateComboBox)
        layout.addLayout(robotMovementHBox)


    def robotMovementChanged(self, text):
        self.notifyObservers(SetJSONVars.MOVEMENT_TYPE, text)

    def makeGraphs(self, layout):
        """
        makes all of the graphs
        """
        self.sensorGraphs = {}
        for sensor in GetJSONVars:
            self.sensorGraphs[sensor] = DataGraph(sensor.value, (-100, 100))
            layout.addWidget(self.sensorGraphs[sensor])

    def makeBeginMatchButton(self, layout):
        button = QPushButton("Begin Match")
        button.clicked.connect(self.startMatch)
        layout.addWidget(button)

    def startMatch(self):
        self.notifyObservers(BehavioralStates.MATCH_START, None)

    def makeEndMatchButton(self, layout):
        button = QPushButton("Match Over")
        button.clicked.connect(self.endMatch)
        layout.addWidget(button)

    def endMatch(self):
        self.notifyObservers(BehavioralStates.END_MATCH, None)

    def makeResetButton(self, layout):
        button = QPushButton("Reset Match")
        button.clicked.connect(self.reset)
        layout.addWidget(button)

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
        index = self.intelligenceStateComboBox.findText(
            IntelligenceStates.IDLE.value, Qt.MatchFixedString)
        if index >= 0:
            self.intelligenceStateComboBox.setCurrentIndex(index)
