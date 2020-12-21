import pytest
from GUI.mainWindow import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from GUI.WindowEnums import WindowEnums
from Guidance.GuidanceEnums import BehavioralStates, IntelligenceStates
from Hardware_Comms.ESPHTTPTopics import SetJSONVars
from Robot_Locomotion.MotorEnums import PWMVals


class Observer(QWidget):
    def __init__(self):
        self.reset()

    def notify(self, topic, value):
        self.data.append((topic, value))

    def reset(self):
        self.data = []


# easier for testing as a global
observer = Observer()


@pytest.fixture
def observerlessWindow(qtbot):
    # TODO True
    window = MainWindow(False)
    qtbot.addWidget(window)

    return window


@pytest.fixture()
def window(qtbot):
    # TODO mmake True
    window = MainWindow(False)
    observer.reset()
    window.attachObserver(observer)
    qtbot.addWidget(window)
    return window


def test_attach_observer(observerlessWindow):
    assert observerlessWindow.observers == []
    observerlessWindow.attachObserver(observer)
    assert observerlessWindow.observers == [observer]


def test_estop(window, qtbot):
    assert observer.data == []
    qtbot.mouseClick(window.ESTOPButton, Qt.LeftButton)
    assert observer.data == [(BehavioralStates.ESTOP, "ESTOP")]


def groupEnabled(enabledButton, disabledButton):
    return enabledButton.isChecked() and not disabledButton.isChecked()


def groupDisabled(enabledButton, disabledButton):
    return not enabledButton.isChecked() and disabledButton.isChecked()


def radio_button_enable_disable_helper(enabledButton, disabledButton, topic, bot):
    # assure initialized to disable
    assert groupDisabled(enabledButton, disabledButton)

    # check enable

    bot.mouseClick(enabledButton, Qt.LeftButton)
    assert groupEnabled(enabledButton, disabledButton)
    assert observer.data == [(topic, 'true')]
    observer.reset()
    assert observer.data == []

    # try to enable again
    bot.mouseClick(enabledButton, Qt.LeftButton)
    assert groupEnabled(enabledButton, disabledButton)
    # won't send an update for no new info
    assert observer.data == []
    observer.reset()
    assert observer.data == []

    # disable
    bot.mouseClick(disabledButton, Qt.LeftButton)
    assert groupDisabled(enabledButton, disabledButton)
    assert observer.data == [(topic, 'false')]
    observer.reset()
    assert observer.data == []

    # disable again
    bot.mouseClick(disabledButton, Qt.LeftButton)
    assert groupDisabled(enabledButton, disabledButton)
    assert observer.data == []
    observer.reset()
    assert observer.data == []


def test_drive_enabled_changed(window, qtbot):
    enabledButton = None
    disabledButton = None

    assert observer.data == []
    # distinguish buttons
    for button in list(window.drive_enabled_group.buttons()):
        label = button.text()
        if label == "Disable Drive":
            disabledButton = button
        elif label == "Enable Drive":
            enabledButton = button
        else:
            assert False
    # make sure buttons were set
    if enabledButton == None or disabledButton == None:
        assert False

    radio_button_enable_disable_helper(enabledButton, disabledButton, SetJSONVars.DRIVE_ENABLE_CHANGE, qtbot)


def test_weapon_enabled_changed(window, qtbot):
    enabledButton = None
    disabledButton = None

    assert observer.data == []
    # distinguish buttons
    for button in list(window.weapon_enabled_group.buttons()):
        label = button.text()
        if label == "Disable Weapon":
            disabledButton = button
        elif label == "Enable Weapon":
            enabledButton = button
        else:
            assert False
    # make sure buttons were set
    if enabledButton == None or disabledButton == None:
        assert False

    radio_button_enable_disable_helper(enabledButton, disabledButton, SetJSONVars.WEAPON_ENABLE_CHANGE, qtbot)


def test_intelligence_state_changed(window, qtbot):
    assert observer.data == []
    index = window.intelligenceStateComboBox.findText(IntelligenceStates.RC.value, Qt.MatchFixedString)
    if index < 0:
        assert False
    # TODO figure out how to do this with qtbot
    window.intelligenceStateComboBox.setCurrentIndex(index)
    window.intelligenceStateChanged(IntelligenceStates.RC.value)
    assert window.intelligenceStateComboBox.currentText() == "Remote Control"
    assert observer.data == [(IntelligenceStates.RC, 'Remote Control'), (WindowEnums.RC, 'RC GUI')]
    observer.reset()


def test_send_pwm(window, qtbot):
    # TODO Get rid of window.motors, only used for testing
    for (lineEdit, button, motor) in window.motors:
        startVal = lineEdit.text()
        assert observer.data == []
        qtbot.keyClicks(lineEdit, "1499")
        qtbot.mouseClick(button, Qt.LeftButton)
        assert observer.data == [(BehavioralStates.PWM, (motor, '1500'))]
        observer.reset()
        tooHigh = int(PWMVals.FULL_CW.value) + 1000
        qtbot.keyClicks(lineEdit, str(tooHigh))
        qtbot.mouseClick(button, Qt.LeftButton)
        assert observer.data == [(BehavioralStates.PWM, (motor, startVal))]
        observer.reset()
        tooLow = int(PWMVals.FULL_CCW.value) - 1000
        qtbot.keyClicks(lineEdit, str(tooLow))
        qtbot.mouseClick(button, Qt.LeftButton)
        assert observer.data == [(BehavioralStates.PWM, (motor, startVal))]
        observer.reset()


def test_send_movement(window, qtbot):
    assert observer.data == []
    assert "3" == window.movementQLineEdit.text()
    qtbot.mouseClick(window.movementButton, Qt.LeftButton)
    assert observer.data == [(BehavioralStates.MOVEMENT_TEST, 3)]
    observer.reset()
    qtbot.keyClick(window.movementQLineEdit, Qt.Key_Backspace)
    qtbot.keyClicks(window.movementQLineEdit, "0")
    qtbot.mouseClick(window.movementButton, Qt.LeftButton)
    assert "0" == window.movementQLineEdit.text()
    assert observer.data == []
    observer.reset()
    qtbot.keyClick(window.movementQLineEdit, Qt.Key_Backspace)
    qtbot.keyClicks(window.movementQLineEdit, "5")
    qtbot.mouseClick(window.movementButton, Qt.LeftButton)
    assert "5" == window.movementQLineEdit.text()
    assert observer.data == [(BehavioralStates.MOVEMENT_TEST, 5)]
    observer.reset()


def test_notify_observers(window):
    assert observer.data == []
    window.notifyObservers("hello!", "world")
    assert observer.data == [("hello!", "world")]


def test_set_state_to_idle(window):
    assert window.intelligenceStateComboBox.currentText() == IntelligenceStates.IDLE.value
    window.intelligenceStateComboBox.setCurrentIndex(1)
    window.intelligenceStateChanged(IntelligenceStates.RC.value)
    assert window.intelligenceStateComboBox.currentText() == IntelligenceStates.RC.value
    window.setStateToIdle()
    assert window.intelligenceStateComboBox.currentText() == IntelligenceStates.IDLE.value
