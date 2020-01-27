#!/usr/bin/python3
import sys
import os
from shutil import copyfile
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
        self.imageIter = iter(images)

        # Retriving all of the file names and appending them to the list
        for f_name in os.listdir(self.inputPath):
            if f_name.endswith('.jpg'):
                images.append(f_name)

        # Creating a label and pixmap object to use to display our images and initializing the first image
        self.label = QLabel(self)
        self.currentImage = next(self.imageIter)
        self.pixmap = QPixmap(self.inputPath + "/" + self.currentImage)
        self.label.setPixmap(self.pixmap)
        self.label.adjustSize()
        self.label.move(160, 0)


    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Left:
            self.leftHandler()
        elif event.key() == Qt.Key_Right:
            self.rightHandler()
        elif event.key() == Qt.Key_Up:
            self.upHandler()

    # The Picture is Green
    def leftHandler(self):

        # Copying the file to the correct directory
        copyfile(self.inputPath + "/" + self.currentImage, self.greenPath + "/" + self.currentImage)

        # Iterating the image list and setting the new picture
        try:
            self.currentImage = next(self.imageIter)
            self.pixmap = QPixmap(self.inputPath + "/" + self.currentImage)
            self.label.setPixmap(self.pixmap)
        except StopIteration:
            print("Done!")
    
    # The Picture is Yellow
    def rightHandler(self):

        # Copying the file to the correct directory
        copyfile(self.inputPath + "/" + self.currentImage, self.yellowPath + "/" + self.currentImage)

        # Iterating the image list and setting the new picture
        try:
            self.currentImage = next(self.imageIter)
            self.pixmap = QPixmap(self.inputPath + "/" + self.currentImage)
            self.label.setPixmap(self.pixmap)
        except StopIteration:
            print("Done!")
    
    # The Picture is an Open
    def upHandler(self):

        # Copying the file to the correct directory
        copyfile(self.inputPath + "/" + self.currentImage, self.openPath + "/" + self.currentImage)

        # Iterating the image list and setting the new picture
        try:
            self.currentImage = next(self.imageIter)
            self.pixmap = QPixmap(self.inputPath + "/" + self.currentImage)
            self.label.setPixmap(self.pixmap)
        except StopIteration:
            print("Done!")

if __name__ == '__main__':
    
    # GUI Setup
    app = QApplication(sys.argv)

    # Open Window
    w = Window()
    w.show()

    # System Exit on window close
    sys.exit(app.exec_())