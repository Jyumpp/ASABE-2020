#!/usr/bin/python3

import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QLineEdit, QLabel, QMainWindow, QAction
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot

class InputWindow(QMainWindow):

    def __init__(self):
        
        super().__init__()
        self.initUI()

    def initUI(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Setting the window title
        self.setWindowTitle('Auto Sort')
        self.resize(640, 480)

        # Setting up sort button and fields
        self.sort = QPushButton('Sort!', self)
        self.sort.resize(80, 40)
        self.sort.move(280, 420)
        self.sort.clicked.connect(self.on_click)

        # Input Path Field
        self.InputPathBox = QLineEdit(self)
        self.InputPathBox.move(55, 60)
        self.InputPathBox.resize(530, 25)

        self.InputLabel = QLabel(self)
        self.InputLabel.setText('Input Directory:')
        self.InputLabel.move(55, 42)

        # Green Path Field
        self.GreenPathBox = QLineEdit(self)
        self.GreenPathBox.move(55, 120)
        self.GreenPathBox.resize(530, 25)

        self.GreenLabel = QLabel(self)
        self.GreenLabel.setText('Green Plant Directory:')
        self.GreenLabel.move(55, 102)

        # Yellow Path Field
        self.YellowPathBox = QLineEdit(self)
        self.YellowPathBox.move(55, 180)
        self.YellowPathBox.resize(530, 25)

        self.YellowLabel = QLabel(self)
        self.YellowLabel.setText('Yellow Plant Directory:')
        self.YellowLabel.move(55, 162)

        # Open Path Field
        self.OpenPathBox = QLineEdit(self)
        self.OpenPathBox.move(55, 240)
        self.OpenPathBox.resize(530, 25)

        self.OpenLabel = QLabel(self)
        self.OpenLabel.setText('No Plant Directory:')
        self.OpenLabel.move(55, 222)

        # Showing our window
        self.show()

    # Button Click Event Handler
    @pyqtSlot()
    def on_click(self):
        self.InputPath = self.InputPathBox.text()
        self.GreenPath = self.GreenPathBox.text()
        self.YellowPath = self.YellowPathBox.text()
        self.OpenPath = self.OpenPathBox.text()

if __name__ == '__main__':
    
    # GUI Setup
    app = QApplication(sys.argv)

    # System Exit on window close
    sys.exit(app.exec_())

    # Open Input Window
    InputWindow = InputWindow()

    # Do File Searching/Collection

    # Open Picture Sorting Window


    


