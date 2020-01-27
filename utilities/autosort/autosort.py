#!/usr/bin/python3
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QMainWindow, QAction, QFileDialog
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap

# Declaring Global Variables

class Window(QMainWindow):

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

        # Input Directory Dialog
        self.inputPath = str(QFileDialog.getExistingDirectory(self, "Select Input Directory"))
        # Green Directory Dialog
        self.greenPath = str(QFileDialog.getExistingDirectory(self, "Select Green Output Directory"))
        # Yellow Directory Dialog
        self.yellowPath = str(QFileDialog.getExistingDirectory(self, "Select Yellow Output Directory"))
        # Open Directory Dialog
        self.openPath = str(QFileDialog.getExistingDirectory(self, "Select Open Output Directory"))
        
        # Initializing a list to hold all of the image file names
        images = []

        # Creating an iterator for our list
        imageIter = iter(images)

        # Retriving all of the file names and appending them to the list
        for f_name in os.listdir(self.inputPath):
            if f_name.endswith('.jpg'):
                images.append(f_name)

        # Creating a label and pixmap object to use to display our images and initializing the first image
        label = QLabel(self)
        pixmap = QPixmap(self.inputPath + "/" + next(imageIter))
        label.setPixmap(pixmap)


    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Left:
            self.leftHandler()
        elif event.key() == Qt.Key_Right:
            self.rightHandler()
        elif event.key() == Qt.Key_Up:
            self.upHandler()

    
    def leftHandler(self):
        print("Left\n")
    
    def rightHandler(self):
        print("Right\n")
    
    def upHandler(self):
        print("Up\n")

if __name__ == '__main__':
    
    # GUI Setup
    app = QApplication(sys.argv)

    # Open Window
    w = Window()
    w.show()

    # System Exit on window close
    sys.exit(app.exec_())