from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QComboBox, QLabel, QSlider, QLineEdit
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import pyqtSlot, Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("Basic GUI")
        self.setGeometry(100, 100, 600, 400) 
        self.spacing = 20 #num pixels between widgets

        self.makeButtons()
        self.makeComboBoxes()
        self.makeSliders()

        
    def makeButtons(self):
        ESTOPButton = QPushButton(self.mainWidget)
        ESTOPButton.setText("Estop")
        ESTOPButton.move(64,32)
        ESTOPButton.clicked.connect(self.ESTOP)


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

        sliderX, sliderY = 300,300
        pwmLabel = QLabel(self.mainWidget)
        pwmLabel.setText("PWM")
        pwmLabel.move(sliderX, sliderY)
        pwmLabelHeight = self.getLabelHeight(pwmLabel)


        self.pwmQLineEdit = QLineEdit(self.mainWidget)
        self.pwmQLineEdit.setValidator(QIntValidator())
        self.pwmQLineEdit.setMaxLength(3)
        self.pwmQLineEdit.textEdited.connect(self.PWMValueChanged)
        self.pwmQLineEdit.move(sliderX, sliderY + pwmLabelHeight + self.spacing )
        qEditWidth = 100
        self.pwmQLineEdit.setFixedWidth(qEditWidth)

        self.pwmSlider = QSlider(Qt.Horizontal, self.mainWidget)
        self.pwmSlider.setRange(0,100)
        self.pwmSlider.setSingleStep(1)
        self.pwmSlider.valueChanged.connect(self.PWMValueChanged)
        self.pwmSlider.move(sliderX + self.spacing + qEditWidth, sliderY + pwmLabelHeight + self.spacing)
        self.pwmSlider.setFixedWidth(500)

    
    def getLabelHeight(self, label):
        return label.fontMetrics().boundingRect(label.text()).height()


    def getLabelWidth(self, label):
        return label.fontMetrics().boundingRect(label.text()).width()

    
    def PWMValueChanged(self, value):
        self.pwmSlider.setValue(int(value))
        self.pwmQLineEdit.setText(str(value))
        print("PWM is now %d" % value)


    def intelligenceStateChanged(self, text):
        print(text)


    def ESTOP(self):
        print("ESTOP")