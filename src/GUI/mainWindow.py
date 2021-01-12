from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow,
                             QComboBox, QLabel, QButtonGroup,
                             QHBoxLayout, QVBoxLayout, QLineEdit,
                             QRadioButton)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from src.Guidance.GuidanceEnums import IntelligenceStates_T, BehavioralStates_T
from src.Hardware_Comms.ESPHTTPTopics import SetJSONVars_T, GetJSONVars_T
from src.Robot_Locomotion.MotorEnums import PWMVals_T
from src.GUI.WindowEnums_T import WindowEnums_T
from src.GUI.DataGraph import DataGraph
from src.Sensing.RobotDataManager import RobotDataManager


class MainWindow(QMainWindow):
    """
    This class contains a main window for the application.
    """

    def __init__(self, GUI_graphs):
        """
        init initializes the QWidgets and sets the geometry of the window
        :param GUI_graphs: [Bool] True to display graphs, False otherwise
        """
        super().__init__()

        self.has_graphs = GUI_graphs

        # make main window
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Basic GUI")

        # important for setting locations of QWidgets
        self.observers = []

        self.initializeLayout()
        self.main_widget.setLayout(self.layout)

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
        for label in self.sensor_labels.values():
            label[1].setText("0")

    def initializeLayout(self):
        """
        sets the locations of all widgets on the GUI
        """
        self.layout = QHBoxLayout(self.main_widget)
        first_col = QVBoxLayout(self.main_widget)

        # add widgets to first col
        self.makeESTOP_Button(first_col)
        self.makeRobotSystemEnablingButtons(first_col)
        self.makeIntelligenceStateComboBox(first_col)
        self.makePWMButtons(first_col)
        self.makePolygonalMovement(first_col)
        self.makeSensorLabels(first_col)

        self.layout.addLayout(first_col)

        if self.has_graphs:
            second_col = QVBoxLayout(self.main_widget)
            self.makeGraphs(second_col)
            self.layout.addLayout(second_col)

        thirdCol = QVBoxLayout(self.main_widget)
        self.makeBeginMatchButton(thirdCol)
        self.makeEndMatchButton(thirdCol)
        self.makeResetButton(thirdCol)
        self.layout.addLayout(thirdCol)

    def makeESTOP_Button(self, layout):
        """
        make the ESTOP button and add it to layout
        :param layout: the layout to add the ESTOP to
        """
        self.ESTOP_Button = QPushButton(self.main_widget)
        self.ESTOP_Button.setText("Estop")
        self.ESTOP_Button.clicked.connect(self.ESTOP)

        layout.addWidget(self.ESTOP_Button)

    def ESTOP(self):
        """
        alerts observers that an ESTOP is requested
        """
        self.notifyObservers(BehavioralStates_T.ESTOP, "ESTOP")

    def makeRobotSystemEnablingButtons(self, layout):
        """
        makes the radio buttons that toggle drive enabled on/pff
        :param layout: the layout to add the radio buttons to
        """
        # dict of label to params for notifying of click (topic, value)
        # For testing
        self.enabling_buttons = []

        self.enabling_labels = {}
        self.enabling_labels["Disable Drive"] = (
            SetJSONVars_T.DRIVE_ENABLE_CHANGE, "false")
        self.enabling_labels["Enable Drive"] = (
            SetJSONVars_T.DRIVE_ENABLE_CHANGE, "true")
        self.enabling_labels["Disable Weapon"] = (
            SetJSONVars_T.WEAPON_ENABLE_CHANGE, "false")
        self.enabling_labels["Enable Weapon"] = (
            SetJSONVars_T.WEAPON_ENABLE_CHANGE, "true")

        drive_radio_h_box = QHBoxLayout(self.main_widget)
        self.drive_enabled_group = QButtonGroup()
        weapon_radio_h_box = QHBoxLayout(self.main_widget)
        self.weapon_enabled_group = QButtonGroup()

        count = 0
        for label in self.enabling_labels.keys():
            button = self.makeRadioButton(label)
            if count < 2:
                drive_radio_h_box.addWidget(button)
                self.drive_enabled_group.addButton(button)
            else:
                weapon_radio_h_box.addWidget(button)
                self.weapon_enabled_group.addButton(button)
            if count % 2 == 0:
                button.setChecked(True)
            else:
                button.setChecked(False)
            count += 1

        layout.addLayout(drive_radio_h_box)
        layout.addLayout(weapon_radio_h_box)

    def makeRadioButton(self, label):
        """
        makes a radio button
        is in a function cuz python loop scope bad
        :param label: [String]
        :return: [QRadioButton] the button
        """
        button = QRadioButton(label, self.main_widget)
        button.toggled.connect(lambda: self.enableChanged(button))
        self.enabling_buttons.append(button)
        return button

    def enableChanged(self, button):
        """
        callback for system enabled radio buttons (drive, weapon)
        :param arm_button: [QRadioButton] the button that's been changed
        """
        if button.isChecked():
            if button.text() in self.enabling_labels.keys():
                params = self.enabling_labels[button.text()]
                self.notifyObservers(params[0], params[1])

    def makeIntelligenceStateComboBox(self, layout):
        # make label
        label = QLabel(self.main_widget)
        label.setText("Intelligence State")

        # make combobox
        # Is self because setToIdle needs it
        self.intelligence_state_combo_box = QComboBox(self.main_widget)
        self.intelligence_state_combo_box.addItems(IntelligenceStates_T.list_states())
        self.intelligence_state_combo_box.activated[str].connect(self.intelligenceStateChanged)

        # followed by intelligence state combo box
        intelligence_hbox = QHBoxLayout(self.main_widget)
        intelligence_hbox.addWidget(label)
        intelligence_hbox.addWidget(self.intelligence_state_combo_box)
        layout.addLayout(intelligence_hbox)

    def intelligenceStateChanged(self, text):
        """
        notfies observers of change in intelligence state
        :param text: [String] The new intelligence state (must correspond to an IntelligenceStateEnum)
        """
        state = None
        for s in IntelligenceStates_T:
            if text == s.value:
                state = s
                break
        self.notifyObservers(state, text)
        if state == IntelligenceStates_T.RC:
            self.notifyObservers(WindowEnums_T.RC, WindowEnums_T.RC.value)

    def makePWMButtons(self, layout):
        """
        creates all the push buttons
        """
        self.motors = []
        pwm_label = QLabel(self.main_widget)
        pwm_label.setText("Individually set PWMs")
        layout.addWidget(pwm_label)

        motors = [SetJSONVars_T.MOTOR1_PWM,
                  SetJSONVars_T.MOTOR2_PWM, SetJSONVars_T.WEAPON_PWM]

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
        q_edit_width = 100

        h_box = QHBoxLayout(self.main_widget)
        validator = QIntValidator(
            int(PWMVals_T.FULL_CCW.value), int(PWMVals_T.FULL_CW.value))
        pwm_input = QLineEdit(PWMVals_T.STOPPED.value, self.main_widget)
        pwm_input.setValidator(validator)
        pwm_input.setMaxLength(4)
        pwm_input.setFixedWidth(q_edit_width)
        h_box.addWidget(pwm_input)

        send_pwm_button = QPushButton(self.main_widget)
        label = "Set PWM for " + motor.value
        send_pwm_button.setText(label)
        send_pwm_button.clicked.connect(lambda: self.sendPWM(pwm_input, motor))
        h_box.addWidget(send_pwm_button)
        self.motors.append((pwm_input, send_pwm_button, motor))
        return h_box

    def sendPWM(self, q_line_edit, motor):
        """
        alerts observers of change in pwm
        """
        val = int(q_line_edit.text())
        if val < int(PWMVals_T.FULL_CCW.value) or val > int(PWMVals_T.FULL_CW.value):
            print(
                "Not sending. Value not in range. Range is " + PWMVals_T.FULL_CCW.value
                + " to " + PWMVals_T.FULL_CW.value)
            if val < int(PWMVals_T.FULL_CCW.value):
                val = PWMVals_T.FULL_CCW.value
            else:
                val = PWMVals_T.FULL_CW.value
        self.notifyObservers(BehavioralStates_T.PWM, (motor, str(val)))

    def makePolygonalMovement(self, layout):
        label = QLabel(self.main_widget)
        label.setText("Drive polygon, n sides")
        layout.addWidget(label)

        # callback needs this to be self
        h_box = QHBoxLayout(self.main_widget)
        self.movement_q_line_edit = QLineEdit("3", self.main_widget)
        self.movement_q_line_edit.setValidator(QIntValidator())
        self.movement_q_line_edit.setMaxLength(1)
        h_box.addWidget(self.movement_q_line_edit)

        self.movement_button = QPushButton(self.main_widget)
        self.movement_button.setText("Send Movement Info")
        self.movement_button.clicked.connect(self.sendMovement)
        h_box.addWidget(self.movement_button)
        layout.addLayout(h_box)

    def sendMovement(self):
        """
        notifies observers of change in movement desired with desired value
        """
        value = self.movement_q_line_edit.text()
        if not value or int(value) < 3:
            print("Polygon needs at least 2 sides")
            return
        self.notifyObservers(BehavioralStates_T.MOVEMENT_TEST, int(value))

    def makeSensorLabels(self, layout):
        self.sensor_labels = {}
        for sensor in GetJSONVars_T:
            h_box = QHBoxLayout(self.main_widget)

            label = QLabel(self.main_widget)
            label.setFixedWidth(300)
            label.setText(sensor.value)
            h_box.addWidget(label)

            data = QLabel(self.main_widget)
            data.setText("   0")
            h_box.addWidget(data)

            layout.addLayout(h_box)
            self.sensor_labels[sensor] = (label, data)

    def makeGraphs(self, layout):
        """
        makes all of the graphs
        """
        self.sensor_graphs = {}
        for sensor in GetJSONVars_T:
            self.sensor_graphs[sensor] = DataGraph(sensor.value, (-100, 100))
            layout.addWidget(self.sensor_graphs[sensor])

    def makeBeginMatchButton(self, layout):
        button = QPushButton("Begin Match")
        button.clicked.connect(self.startMatch)
        layout.addWidget(button)

    def startMatch(self):
        self.notifyObservers(BehavioralStates_T.MATCH_START, None)

    def makeEndMatchButton(self, layout):
        button = QPushButton("Match Over")
        button.clicked.connect(self.endMatch)
        layout.addWidget(button)

    def endMatch(self):
        self.notifyObservers(BehavioralStates_T.END_MATCH, None)

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
        if topic in GetJSONVars_T:
            # update specific graph
            if self.has_graphs:
                graph = self.sensor_graphs[topic]
                if value != graph.getCurrData():
                    graph.updatePlot(value)

            # update label on GUI
            self.sensor_labels[topic][1].setText(value)

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
        self.intelligenceStateChanged(IntelligenceStates_T.IDLE.value)
        index = self.intelligence_state_combo_box.findText(
            IntelligenceStates_T.IDLE.value, Qt.MatchFixedString)
        if index >= 0:
            self.intelligence_state_combo_box.setCurrentIndex(index)
