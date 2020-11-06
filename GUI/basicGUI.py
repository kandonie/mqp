from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QSlider, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from Hardware_Comms.ESPHTTPTopics import CommsTopics
from Guidance.IntelligenceState import IntelligenceState

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
        self.setGeometry(100, 100, 600, 600)

        #important for setting locations of QWidgets
        self.spacing = 20 #num pixels between widgets
        self.observers= []

        #make widgets
        self.makeButtons()
        self.makeComboBoxes()
        self.makeSliders()
        self.makeLabels()

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
        ESTOPButton = QPushButton(self.mainWidget)
        ESTOPButton.setText("Estop")
        ESTOPButton.move(64,32)
        ESTOPButton.clicked.connect(self.ESTOP)

        #make send PWM button
        sendPWMButton = QPushButton(self.mainWidget)
        sendPWMButton.setText("Send PWM")
        sendPWMButton.move(100, 400)
        sendPWMButton.clicked.connect(self.sendPWM)


    def makeComboBoxes(self):
        """makes the Intelligence state combo box, along with corresponding label
        """        
        #make label
        intelligenceStateComboBoxLabel = QLabel(self.mainWidget)
        intelligenceStateComboBoxLabel.move(100,100)
        intelligenceStateComboBoxLabel.setText("Intelligence State")
        labelWidth = self.getLabelWidth(intelligenceStateComboBoxLabel)

        #make combobox
        intelligenceStateComboBox = QComboBox(self.mainWidget)
        #addd in each state in intelligence state as an option
        options = []
        for state in IntelligenceState:
            options.append(str(state.name))
        intelligenceStateComboBox.addItems(options)
        #finalize box
        intelligenceStateComboBox.activated[str].connect(self.intelligenceStateChanged)
        intelligenceStateComboBox.move(100 + labelWidth + self.spacing, 100)

    
    def makeSliders(self):
        """makes a PWM slider
        """        
        #create pwm slider label (just shows the word PWM over the slider) 
        sliderX, sliderY = 100,200
        pwmLabel = QLabel(self.mainWidget)
        pwmLabel.setText("PWM")
        pwmLabel.move(sliderX, sliderY)
        pwmLabelHeight = self.getLabelHeight(pwmLabel)

        #create pwm qedit (corresponds to value of slider)
        self.pwmQLineEdit = QLineEdit("0", self.mainWidget)
        qEditWidth = 100
        self.pwmQLineEdit.setFixedWidth(qEditWidth)
        self.pwmQLineEdit.setValidator(QIntValidator())
        self.pwmQLineEdit.setMaxLength(3)
        self.pwmQLineEdit.textEdited.connect(self.PWMValueChanged)
        self.pwmQLineEdit.move(sliderX, sliderY + pwmLabelHeight + self.spacing )

        #create pwm slider (corresponds to value of QLineEdit)
        self.pwmSlider = QSlider(Qt.Horizontal, self.mainWidget)
        self.pwmSlider.setRange(0,100)
        self.pwmSlider.setSingleStep(1)
        self.pwmSlider.valueChanged.connect(self.PWMValueChanged)
        self.pwmSlider.move(sliderX + self.spacing + qEditWidth, sliderY + pwmLabelHeight + self.spacing)
        self.pwmSlider.setFixedWidth(500)


    def makeLabels(self):
        """makes labels for data read
        """        
        #angular position label
        aPosLabel = QLabel(self.mainWidget)
        aPosDataLabel = QLabel(self.mainWidget)
        aPosLabel.setText("Angular Position: ")
        aPosDataLabel.setText(str(self.getAPos()))
        aPosLabel.move(100, 500)
        aPosDataLabel.move(100 + self.getLabelWidth(aPosLabel) + self.spacing, 500)

    
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
        self.notify(CommsTopics.SET_PWM, self.pwmQLineEdit.text())

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
        self.notify(CommsTopics.INTELLIGENCE_STATE, text)

    def ESTOP(self):
        """alerts observers that an ESTOP is requested
        """
        self.notify(CommsTopics.ESTOP, "ESTOP")

    def notify(self, topic, value):
        """notifies observers of topic with value

        Args:
            topic (CommsTopics): a communication topic 
            value (string): the value for the comm topic
        """
        for observer in self.observers:
            observer.notify(topic, value)