import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QLineEdit, QPushButton,QVBoxLayout)
from functools import partial


ERROR_MSG = 'ERROR'

"""Below class functions as View of MVP model, job of which is 
    to provide the frontend"""
class PyCalcUi(QMainWindow):
    def __init__(self):
        super().__init__()

        #Window properties
        self.setWindowTitle('PyCalc')
        self.setFixedSize(235, 235)

        #General Layout
        self.generalLayout = QVBoxLayout()

        #Central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()
    def _createDisplay(self):
        #Create the QLineEdit object
        self.display = QLineEdit()

        #Configure the display
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)

        #Add display to general layout
        self.generalLayout.addWidget(self.display)
    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {'7': (0, 0), '8': (0, 1), '9': (0, 2), '/': (0, 3), 'C': (0, 4),
                   '4': (1, 0), '5': (1, 1), '6': (1, 2), '*': (1, 3), '(': (1, 4),
                   '1': (2, 0), '2': (2, 1), '3': (2, 2), '-': (2, 3), ')': (2, 4),
                   '0': (3, 0), '00': (3, 1), '.': (3, 2), '+': (3, 3),'=': (3, 4),
                  }
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40,40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0],pos[1])
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        # Set display's text
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        # Get display's text
        return self.display.text()

    def clearDisplay(self):
        #Clear the display.
        self.setDisplayText('')


"""This class is the Controller that regulates the connection between Model and View"""
class PyCalcCtrl:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignal()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText()+sub_exp
        self._view.setDisplayText(expression)

    def _connectSignal(self):
        for btnText, btn in self._view.buttons.items():
            if btnText not in ('=', 'C'):
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)


"""Model part is covered by this little function."""
def evaluateExpression(expression):
    try:
        result = str(eval(expression,{}, {}))
    except Exception:
        result = ERROR_MSG
    return result

#Client code
def main():
    pycalc = QApplication(sys.argv)
    vie = PyCalcUi()
    vie.show()
    model = evaluateExpression
    PyCalcCtrl(model=model, view=vie)
    sys.exit(pycalc.exec())


if __name__ == '__main__':
    main()
