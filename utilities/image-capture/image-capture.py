#!/usr/bin/python3
import sys
import os
import time
from PyQt5.Qt import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

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
        self.setWindowTitle('Image-Capture')
        self.resize(1280, 720)

        # Setting up the camera object and getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            pass #quit
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.select_camera(0)

        # Setting up Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Setting up camera selection toolbar
        camera_toolbar = QToolBar("Camera")
        camera_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(camera_toolbar)
        camera_selector = QComboBox()
        camera_selector.addItems([c.description() for c in self.available_cameras])
        camera_selector.currentIndexChanged.connect(self.select_camera)
        camera_toolbar.addWidget(camera_selector)

        # Green Directory Dialog
        self.greenPath = str(QFileDialog.getExistingDirectory(self, "Select Green Output Directory"))
        # Yellow Directory Dialog
        self.yellowPath = str(QFileDialog.getExistingDirectory(self, "Select Yellow Output Directory"))
        # Open Directory Dialog
        self.openPath = str(QFileDialog.getExistingDirectory(self, "Select Open Output Directory"))

    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()

        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda i, e, s: self.alert(s))
        self.capture.imageCaptured.connect(lambda d, i: self.status.showMessage("Image %04d captured" % self.save_seq))

        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_F1:
            self.greenHandler()
        elif event.key() == Qt.Key_F2:
            self.yellowHandler()
        elif event.key() == Qt.Key_F3:
            self.openHandler()

    # The Picture is Green
    def greenHandler(self):

        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.greenPath, "%04d-%s.jpg" % (
            self.save_seq,
            timestamp
        )))
        self.save_seq += 1

        
    
    # The Picture is Yellow
    def yellowHandler(self):

        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.yellowPath, "%04d-%s.jpg" % (
            self.save_seq,
            timestamp
        )))
        self.save_seq += 1
    
    # The Picture is an Open
    def openHandler(self):

        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.openPath, "%04d-%s.jpg" % (
            self.save_seq,
            timestamp
        )))
        self.save_seq += 1
    
    def alert(self, s):
        """
        Handle errors coming from QCamera dn QCameraImageCapture by displaying alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(s)

if __name__ == '__main__':
    
    # GUI Setup
    app = QApplication(sys.argv)

    # Open Window
    w = Window()
    w.show()

    # System Exit on window close
    sys.exit(app.exec_())