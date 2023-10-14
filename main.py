import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.calculator import WindowClass


app = QApplication(sys.argv)
myWindows = WindowClass()
myWindows.show()
sys.exit(app.exec_())