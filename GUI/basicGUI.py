from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QButtonGroup, QLineEdit, QRadioButton
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from Guidance.GuidanceEnums import IntelligenceStates, BehavioralStates
from Hardware_Comms.ESPHTTPTopics import SetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals
from GUI.WindowEnums import WindowEnums

class MainWindow(QMainWindow):
    """This class contains a main window for the application. 
        This is a basic GUI which has simple features.          

    Args:
        QMainWindow: This is of type QMainWindow
    """
    def __init__(self):
        """init initializes the QWidgets and sets the geometry of the window
        """        
        super().__init__()
        #make main window
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("Basic GUI")

        #important for setting locations of QWidgets
        self.observers= []

        #make widgets
        self.makeButtons()
        self.makeComboBoxes()
        self.makeLabels()
        self.makeRadioButtons()

        self.setWidgetLocations()
        print("done GUI creation")

    def setWidgetLocations(self):
        start_x = 50
        start_y = 50
        widgetSpacing = 20 #num pixels between widgets
        sectionSpacing = 60
        #TODO make spacing good and consistent
        #Estop button
        estop_y = start_y
        self.ESTOPButton.move(start_x, estop_y)
        disarm_line1_y = estop_y + self.getLabelHeight(self.ESTOPButton) + sectionSpacing
        #Radio button
        self.disarm_weapon_radio_button.move(start_x, disarm_line1_y)
        armDrive_x = 2 * self.disarm_weapon_radio_button.width() + 2 * sectionSpacing + start_x
        self.arm_weapon_radio_button.move(armDrive_x, disarm_line1_y)
        disarm_line2_y = disarm_line1_y + self.disarm_weapon_radio_button.height() + widgetSpacing
        self.disarm_drive_radio_button.move(start_x, disarm_line2_y)
        armAll_x = 2 * self.disarm_drive_radio_button.width() +  2 * sectionSpacing + start_x
        self.arm_drive_radio_button.move(armAll_x, disarm_line2_y)
        #intelligence state combo box
        intelligenceCombo_y = disarm_line2_y + self.disarm_drive_radio_button.height() + sectionSpacing
        self.intelligenceStateComboBoxLabel.move(start_x, intelligenceCombo_y)
        intelligenceComboLabelWidth = self.getLabelWidth(self.intelligenceStateComboBoxLabel)
        self.intelligenceStateComboBox.move(start_x + intelligenceComboLabelWidth + widgetSpacing, intelligenceCombo_y)
        #PWM for motors
        pwmTitle_y = intelligenceCombo_y + self.getLabelHeight(self.intelligenceStateComboBoxLabel) + sectionSpacing
        self.pwmLabel.move(start_x, pwmTitle_y)
        pwmLabel1_y = pwmTitle_y + widgetSpacing + self.pwmLabel.height()
        self.motor1_pwmQLineEdit.move(start_x, pwmLabel1_y)
        self.sendMotor1_PWMButton.move(start_x + widgetSpacing + self.motor1_pwmQLineEdit.width(), pwmLabel1_y)
        pwmLabel2_y = pwmLabel1_y + self.sendMotor1_PWMButton.height() + sectionSpacing
        self.motor2_pwmQLineEdit.move(start_x, pwmLabel2_y)
        self.sendMotor2_PWMButton.move(start_x + widgetSpacing + self.motor2_pwmQLineEdit.width(), pwmLabel2_y)
        pwmLabel3_y = pwmLabel2_y + self.sendMotor2_PWMButton.height() + sectionSpacing
        self.weapon_pwmQLineEdit.move(start_x, pwmLabel3_y)
        self.sendWeaponPWMButton.move(start_x + widgetSpacing + self.weapon_pwmQLineEdit.width(), pwmLabel3_y)
        #Movement
        movementLabel_y = pwmLabel3_y + self.getLabelHeight(self.sendMotor1_PWMButton) + 2*sectionSpacing
        self.movementLabel.move(start_x, movementLabel_y)
        self.movementTypeButton.move(start_x + self.getLabelWidth(self.movementLabel) + widgetSpacing, movementLabel_y)
        chooseMovement_y = movementLabel_y + 2 * self.getLabelHeight(self.movementTypeButton) + widgetSpacing
        self.movementQLineEdit.move(start_x, chooseMovement_y)
        #sensor info
        sensor_y = chooseMovement_y + 2 * self.movementQLineEdit.height() + sectionSpacing
        self.aPosLabel.move(start_x, sensor_y)
        self.aPosDataLabel.move(start_x + self.getLabelWidth(self.aPosLabel) + widgetSpacing, sensor_y)

        #TODO actually use these
        max_y = sensor_y + 2 * self.getLabelHeight(self.aPosLabel) + widgetSpacing
        max_x = armAll_x + self.arm_drive_radio_button.width() + widgetSpacing
        self.setGeometry(start_x, start_y, 1000, max_y)

    def makeRadioButtons(self):
        self.disarm_weapon_radio_button = QRadioButton("DISARM_WEAPON", self.mainWidget)
        self.disarm_weapon_radio_button.toggled.connect(lambda:self.changeInWeaponArm(self.disarm_weapon_radio_button))
        self.arm_weapon_radio_button = QRadioButton("ARM_WEAPON", self.mainWidget)
        self.arm_weapon_radio_button.toggled.connect(lambda:self.changeInWeaponArm(self.arm_weapon_radio_button))
        self.disarm_drive_radio_button = QRadioButton("DISARM DRIVE", self.mainWidget)
        self.disarm_drive_radio_button.toggled.connect(lambda: self.changeInDriveArm(self.disarm_drive_radio_button))
        self.arm_drive_radio_button = QRadioButton("ARM DRIVE", self.mainWidget)
        self.arm_drive_radio_button.toggled.connect(lambda: self.changeInDriveArm(self.arm_drive_radio_button))
        #Group
        self.weapon_armed_group = QButtonGroup()
        self.drive_armed_group = QButtonGroup()
        self.weapon_armed_group.addButton(self.disarm_weapon_radio_button)
        self.weapon_armed_group.addButton(self.arm_weapon_radio_button)
        self.drive_armed_group.addButton(self.disarm_drive_radio_button)
        self.drive_armed_group.addButton(self.arm_drive_radio_button)
        #start in the disarm state
        self.disarm_weapon_radio_button.setChecked(True)
        self.disarm_drive_radio_button.setChecked(True)


    def changeInDriveArm(self, arm_button):
        if arm_button.isChecked():
            if arm_button == self.arm_drive_radio_button:
                self.notifyObservers(SetJSONVars.ARM_DRIVE, "true")
            else:
                self.notifyObservers(SetJSONVars.ARM_DRIVE, "false")

    def changeInWeaponArm(self, arm_button):
        if arm_button.isChecked():
            if arm_button == self.arm_weapon_radio_button:
                self.notifyObservers(SetJSONVars.ARM_WEAPON, "true")
            else:
                self.notifyObservers(SetJSONVars.ARM_WEAPON, "false")


    def attachObserver(self, observer):
        """adds an of observers to its own list

        Args:
            observer (Observer): must have a notify function that takes 2 args.
                 It's notify will be called upon information changes
        """        
        self.observers.append(observer)
        
    def makeButtons(self):
        """Creates the ESTOP and sendPWM buttons
        """        
        #make ESTOP
        self.ESTOPButton = QPushButton(self.mainWidget)
        self.ESTOPButton.setText("Estop")
        self.ESTOPButton.clicked.connect(self.ESTOP)

        #make send PWM button
        self.sendMotor1_PWMButton = QPushButton(self.mainWidget)
        self.sendMotor1_PWMButton.setText("Send Motor 1 PWM")
        self.sendMotor1_PWMButton.clicked.connect(lambda: self.sendPWM(self.motor1_pwmQLineEdit, SetJSONVars.MOTOR1_PWM))

        # make send PWM button
        self.sendMotor2_PWMButton = QPushButton(self.mainWidget)
        self.sendMotor2_PWMButton.setText("Send Motor 2 PWM")
        self.sendMotor2_PWMButton.clicked.connect(lambda: self.sendPWM(self.motor2_pwmQLineEdit, SetJSONVars.MOTOR2_PWM))

        # make send PWM button
        self.sendWeaponPWMButton = QPushButton(self.mainWidget)
        self.sendWeaponPWMButton.setText("Send Weapon PWM")
        self.sendWeaponPWMButton.clicked.connect(lambda: self.sendPWM(self.weapon_pwmQLineEdit, SetJSONVars.WEAPON_PWM))




    def makeComboBoxes(self):
        """makes the Intelligence state combo box, along with corresponding label
        """        
        #make label
        self.intelligenceStateComboBoxLabel = QLabel(self.mainWidget)
        self.intelligenceStateComboBoxLabel.setText("Intelligence State")
        #make combobox
        self.intelligenceStateComboBox = QComboBox(self.mainWidget)
        #addd in each state in intelligence state as an option
        intelligenceOptions = []
        for state in IntelligenceStates:
            intelligenceOptions.append(state.value)
        self.intelligenceStateComboBox.addItems(intelligenceOptions)
        #finalize box
        self.intelligenceStateComboBox.activated[str].connect(self.intelligenceStateChanged)

        #straight/turn/square
        self.movementLabel = QLabel(self.mainWidget)
        self.movementLabel.setText("Drive polygon, n sides")
        self.movementQLineEdit = QLineEdit("3", self.mainWidget)
        self.movementQLineEdit.setValidator(QIntValidator())
        self.movementQLineEdit.setMaxLength(1)
        self.movementTypeButton = QPushButton(self.mainWidget)
        self.movementTypeButton.setText("Send Movement Info")
        self.movementTypeButton.clicked.connect(self.sendMovement)


    def makeLabels(self):
        """makes labels for data read
        """        
        #angular position label
        self.aPosLabel = QLabel(self.mainWidget)
        self.aPosDataLabel = QLabel(self.mainWidget)
        self.aPosLabel.setText("Angular Position: ")
        self.aPosDataLabel.setText(str(self.getAPos()))

        self.pwmLabel = QLabel(self.mainWidget)
        self.pwmLabel.setText("Individually set PWMs")
        qEditWidth = 100
        #create pwm qedit (corresponds to value of slider)
        self.motorValidator = QIntValidator(int(PWMVals.FULL_CCW.value), int(PWMVals.FULL_CW.value))
        self.motor1_pwmQLineEdit = QLineEdit(PWMVals.STOPPED.value, self.mainWidget)
        self.motor1_pwmQLineEdit.setValidator(self.motorValidator)
        self.motor1_pwmQLineEdit.setMaxLength(4)
        self.motor1_pwmQLineEdit.setFixedWidth(qEditWidth)
     #   self.motor1_pwmQLineEdit.textEdited.connect(lambda: self.PWMValueChanged(self.motor1_pwmQLineEdit))

        self.motor2_pwmQLineEdit = QLineEdit(PWMVals.STOPPED.value, self.mainWidget)
        self.motor2_pwmQLineEdit.setValidator(self.motorValidator)
        self.motor2_pwmQLineEdit.setMaxLength(4)
        self.motor2_pwmQLineEdit.setFixedWidth(qEditWidth)
      #  self.motor2_pwmQLineEdit.textEdited.connect(lambda: self.PWMValueChanged(self.motor2_pwmQLineEdit))

        self.weapon_pwmQLineEdit = QLineEdit(PWMVals.STOPPED.value, self.mainWidget)
        self.weapon_pwmQLineEdit.setValidator(self.motorValidator)
        self.weapon_pwmQLineEdit.setMaxLength(4)
        self.weapon_pwmQLineEdit.setFixedWidth(qEditWidth)

    def getLabelHeight(self, label):
        """returns the height of a label

        Args:
            label (QLabel): the label to get the height of

        Returns:
            int: the height of the label
        """        
        return label.fontMetrics().boundingRect(label.text()).height()


    def getLabelWidth(self, label):
        """returns the width of a label

        Args:
            label (QLabel): the label to get the width of

        Returns:
            int: the width of the label
        """    
        return label.fontMetrics().boundingRect(label.text()).width()

    def sendPWM(self, qLineEdit, motor):
        """alerts observers of change in pwm
        """
        val = int(qLineEdit.text())
        #TODO maybe implement stuff with self.motorValidator, I couldn't gget it working
        if val < int(PWMVals.FULL_CCW.value) or val > int(PWMVals.FULL_CW.value):
            print("Not sending. Value not in range. Range is " + PWMVals.FULL_CCW.value + " to " + PWMVals.FULL_CW.value)
            return
        self.notifyObservers(BehavioralStates.PWM, (motor, qLineEdit.text()))

    def getAPos(self):
        """gets the angular position of the robot

        Returns:
            int: the angular position of the robot
        """
        #TODO
        return 0

    def intelligenceStateChanged(self, text):
        """notfies observers of change in intelligence state

        Args:
            text (String): The new intelligence state (must correspond to an IntelligenceStateEnum)
        """
        state = None
        for s in IntelligenceStates:
            if text == s.value:
                state = s
                break
        self.notifyObservers(state, text)
        # if state == IntelligenceStates.RC:
        #     self.notifyObservers(WindowEnums.RC, WindowEnums.RC.value)


    def setStateToIdle(self):
        self.intelligenceStateChanged(IntelligenceStates.IDLE.value)
        index = self.intelligenceStateComboBox.findText(IntelligenceStates.IDLE.value, Qt.MatchFixedString)
        if index >= 0:
            self.intelligenceStateComboBox.setCurrentIndex(index)


    def sendMovement(self):
        """
        notifies observers of change in movement desired with desired value
        :param text: the box chosen in the combo box
        :return:
        """
        value = self.movementQLineEdit.text()
        if not value:
            value = '0'
        elif int(value) < 3:
            print("Polygon needs at least 2 sides")
            return
        self.notifyObservers(BehavioralStates.MOVEMENT_TEST, int(value))

    def ESTOP(self):
        """alerts observers that an ESTOP is requested
        """
        self.notifyObservers(BehavioralStates.ESTOP, "ESTOP")

    def notifyObservers(self, topic, value, *args):
        """notifies observers of topic with value

        Args:
            topic (CommsTopics): a communication topic 
            value (string): the value for the comm topic
        """
        for observer in self.observers:
            observer.notify(topic, value)

    def notify(self, topic, value):
        pass
