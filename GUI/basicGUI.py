from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QSlider, QLineEdit
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot, Qt
from Hardware_Comms.WiFiComms import WiFiComms
from Hardware_Comms.ESPHTTPTopics import HTTPTopics

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("Basic GUI")
        self.setGeometry(100, 100, 600, 600)
        self.spacing = 20 #num pixels between widgets
        self.WiFi = WiFiComms()

        self.makeButtons()
        self.makeComboBoxes()
        self.makeSliders()
        self.makeLabels()

        
    def makeButtons(self):
        ESTOPButton = QPushButton(self.mainWidget)
        ESTOPButton.setText("Estop")
        ESTOPButton.move(64,32)
        ESTOPButton.clicked.connect(self.ESTOP)

        sendPWMButton = QPushButton(self.mainWidget)
        sendPWMButton.setText("Send PWM")
        sendPWMButton.move(100, 400)
        sendPWMButton.clicked.connect(self.sendPWM)


    def makeComboBoxes(self):
        intelligenceStateComboBoxLabel = QLabel(self.mainWidget)
        intelligenceStateComboBoxLabel.move(100,100)
        intelligenceStateComboBoxLabel.setText("Intelligence State")
        labelWidth = self.getLabelWidth(intelligenceStateComboBoxLabel)
        intelligenceStateComboBox = QComboBox(self.mainWidget)
        intelligenceStateComboBox.addItems(["IDLE", "RC", "AUTO"])
        intelligenceStateComboBox.activated[str].connect(self.intelligenceStateChanged)
        intelligenceStateComboBox.move(100 + labelWidth + self.spacing, 100)

    
    def makeSliders(self):

        sliderX, sliderY = 100,200
        pwmLabel = QLabel(self.mainWidget)
        pwmLabel.setText("PWM")
        pwmLabel.move(sliderX, sliderY)
        pwmLabelHeight = self.getLabelHeight(pwmLabel)


        self.pwmQLineEdit = QLineEdit("0", self.mainWidget)
        qEditWidth = 100
        self.pwmQLineEdit.setFixedWidth(qEditWidth)
        self.pwmQLineEdit.setValidator(QIntValidator())
        self.pwmQLineEdit.setMaxLength(3)
        self.pwmQLineEdit.textEdited.connect(self.PWMValueChanged)
        self.pwmQLineEdit.move(sliderX, sliderY + pwmLabelHeight + self.spacing )

        self.pwmSlider = QSlider(Qt.Horizontal, self.mainWidget)
        self.pwmSlider.setRange(0,100)
        self.pwmSlider.setSingleStep(1)
        self.pwmSlider.valueChanged.connect(self.PWMValueChanged)
        self.pwmSlider.move(sliderX + self.spacing + qEditWidth, sliderY + pwmLabelHeight + self.spacing)
        self.pwmSlider.setFixedWidth(500)


    def makeLabels(self):
        aPosLabel = QLabel(self.mainWidget)
        aPosDataLabel = QLabel(self.mainWidget)
        aPosLabel.setText("Angular Position: ")
        aPosDataLabel.setText(str(self.getAPos()))
        aPosLabel.move(100, 500)
        aPosDataLabel.move(100 + self.getLabelWidth(aPosLabel) + self.spacing, 500)

    
    def getLabelHeight(self, label):
        return label.fontMetrics().boundingRect(label.text()).height()


    def getLabelWidth(self, label):
        return label.fontMetrics().boundingRect(label.text()).width()

    
    def PWMValueChanged(self, value):
        try:
            self.pwmSlider.setValue(int(value))
        except:
            print("couldn't change slider val")
        try:
            self.pwmQLineEdit.setText(str(value))
        except:
            print("Couldn't set QLINEEDIT")

    def sendPWM(self, val):
        self.WiFi.sendInfo(val, HTTPTopics.PWM)

    def getAPos(self):
        return self.WiFi.getInfo(HTTPTopics.APOS)

    def intelligenceStateChanged(self, text):
        print(text)

    def ESTOP(self):
        print("ESTOP")