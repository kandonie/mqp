from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QSlider, QLineEdit, QRadioButton
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from Guidance.GuidanceEnums import IntelligenceStates, BehavioralStates
from Hardware_Comms.ESPHTTPTopics import ARM, SetJSONVars

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
        self.makeSliders()
        self.makeLabels()
        self.makeRadioButtons()

        self.setWidgetLocations()
        print("done GUI creation")

    def setWidgetLocations(self):
        start_x = 50
        start_y = 50
        widgetSpacing = 20 #num pixels between widgets
        sectionSpacing = 60

        #Estop button
        estop_y = start_y
        self.ESTOPButton.move(start_x, estop_y)
        disarm_line1_y = estop_y + self.getLabelHeight(self.ESTOPButton) + sectionSpacing
        #Radio button
        self.disarm_radio_button.move(start_x, disarm_line1_y)
        armDrive_x = 2 * self.disarm_radio_button.width() + 2 * sectionSpacing + start_x
        self.arm_drive_radio_button.move(armDrive_x, disarm_line1_y)
        disarm_line2_y = disarm_line1_y + self.disarm_radio_button.height() + widgetSpacing
        self.arm_weapon_radio_button.move(start_x, disarm_line2_y)
        armAll_x = 2 * self.arm_weapon_radio_button.width() +  2 * sectionSpacing + start_x
        self.arm_radio_button.move(armAll_x, disarm_line2_y)
        #intelligence state combo box
        intelligenceCombo_y = disarm_line2_y + 2 * self.arm_weapon_radio_button.height() + sectionSpacing
        self.intelligenceStateComboBoxLabel.move(start_x, intelligenceCombo_y)
        intelligenceComboLabelWidth = self.getLabelWidth(self.intelligenceStateComboBoxLabel)
        self.intelligenceStateComboBox.move(start_x + intelligenceComboLabelWidth + widgetSpacing, intelligenceCombo_y)
        #PWM Slider
        sliderLabel_y = intelligenceCombo_y + self.getLabelHeight(self.intelligenceStateComboBoxLabel) + sectionSpacing
        self.pwmLabel.move(start_x, sliderLabel_y)
        self.sendPWMButton.move(start_x + self.pwmLabel.width() + widgetSpacing, sliderLabel_y)
        pwmSlider_y = sliderLabel_y + 2 * self.getLabelHeight(self.pwmLabel) + widgetSpacing
        self.pwmQLineEdit.move(start_x, pwmSlider_y)
        qEditWidth = 100
        self.pwmQLineEdit.setFixedWidth(qEditWidth)
        pwmSlider_x = start_x + widgetSpacing + qEditWidth
        self.pwmSlider.move(pwmSlider_x, pwmSlider_y)
        #Movement
        movementLabel_y = pwmSlider_y + self.getLabelHeight(self.sendPWMButton) + sectionSpacing
        self.movementLabel.move(start_x, movementLabel_y)
        self.movementTypeButton.move(start_x + self.getLabelWidth(self.movementLabel) + widgetSpacing, movementLabel_y)
        chooseMovement_y = movementLabel_y + 2 * self.getLabelHeight(self.movementTypeButton) + widgetSpacing
        self.movementQLineEdit.move(start_x, chooseMovement_y)
        #sensor info
        sensor_y = chooseMovement_y + 2 * self.movementQLineEdit.height() + sectionSpacing
        self.aPosLabel.move(start_x, sensor_y)
        self.aPosDataLabel.move(start_x + self.getLabelWidth(self.aPosLabel) + widgetSpacing, sensor_y)

        max_y = sensor_y + 2 * self.getLabelHeight(self.aPosLabel) + widgetSpacing
        max_x = armAll_x + self.arm_radio_button.width() + widgetSpacing
        self.setGeometry(start_x, start_y, 1000, 1000)

    def makeRadioButtons(self):
        self.disarm_radio_button = QRadioButton( ARM.DISARM_ALL.value, self.mainWidget)
        self.disarm_radio_button.toggled.connect(lambda:self.changeInArm(self.disarm_radio_button))
        self.arm_drive_radio_button = QRadioButton(ARM.ARM_DRIVE.value, self.mainWidget)
        self.arm_drive_radio_button.toggled.connect(lambda:self.changeInArm(self.arm_drive_radio_button))
        self.arm_weapon_radio_button = QRadioButton(ARM.ARM_WEAPON.value, self.mainWidget)
        self.arm_weapon_radio_button.toggled.connect(lambda: self.changeInArm(self.arm_weapon_radio_button))
        self.arm_radio_button = QRadioButton(ARM.ARM_ALL.value,self.mainWidget)
        self.arm_radio_button.toggled.connect(lambda: self.changeInArm(self.arm_radio_button))
        #start in the disarm state
        self.disarm_radio_button.setChecked(True)

    def changeInArm(self, arm_button):
        if arm_button.isChecked():
            self.notifyObservers(SetJSONVars.ARM_DISARM_SYSTEMS, arm_button.text())


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
        self.sendPWMButton = QPushButton(self.mainWidget)
        self.sendPWMButton.setText("Send PWM")
        self.sendPWMButton.clicked.connect(self.sendPWM)


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

    
    def makeSliders(self):
        """makes a PWM slider
        """        
        #create pwm slider label (just shows the word PWM over the slider) 
        self.pwmLabel = QLabel(self.mainWidget)
        self.pwmLabel.setText("PWM")

        #create pwm qedit (corresponds to value of slider)
        self.pwmQLineEdit = QLineEdit("1660", self.mainWidget)
        self.pwmQLineEdit.setValidator(QIntValidator())
        self.pwmQLineEdit.setMaxLength(4)
        self.pwmQLineEdit.textEdited.connect(self.PWMValueChanged)

        #create pwm slider (corresponds to value of QLineEdit)
        self.pwmSlider = QSlider(Qt.Horizontal, self.mainWidget)
        self.pwmSlider.setRange(1000, 2000)
        self.pwmSlider.setSingleStep(1)
        self.pwmSlider.valueChanged.connect(self.PWMValueChanged)
        self.pwmSlider.setFixedWidth(500)


    def makeLabels(self):
        """makes labels for data read
        """        
        #angular position label
        self.aPosLabel = QLabel(self.mainWidget)
        self.aPosDataLabel = QLabel(self.mainWidget)
        self.aPosLabel.setText("Angular Position: ")
        self.aPosDataLabel.setText(str(self.getAPos()))

    
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
    
    def PWMValueChanged(self, value):
        """a callback for when pwm value is changed
        ensures the slider and qlineEdit agree
        ensures value is in range [0,100]

        Args:
            value (int): the new Pwm value
        """
        if not value:
            return
        elif int(value) > 100:
            value = 100
        self.pwmSlider.setValue(int(value))
        self.pwmQLineEdit.setText(str(value))

    def sendPWM(self):
        """alerts observers of change in pwm
        """
        self.notifyObservers(BehavioralStates.PWM, self.pwmQLineEdit.text())

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