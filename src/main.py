"""

Time Tracker by Paracosmos Studio.

A simple time tracking application built with PyQt6 that allows 
users to track time spent on different projects.

Version : 1.0.0
License : MIT

"""


import sys
from PyQt6.QtWidgets import QApplication
from interface import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
