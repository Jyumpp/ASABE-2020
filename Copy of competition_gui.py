# -*- coding: utf-8 -*-
# Python 3.7
# This is a simple GUI for the 2020 ASABE Student Robotics Competition.
# Click 'Standard' or 'Advanced' to generate random germination statuses for the corresponding level.
# Meanwhile, the 5-min timer is started, and a background TCP server will accept connection from the IP address selected in the drop-down menu.
# The robot needs to periodically send the detection result so that the server can know that the robot is alive.
# If the server does not receive a message for more than 5 seconds, the server closes the connection.
# We recommend that the robot send a message every second.
# But the robot can connect to the server again after disconnection.
# The message should consist of 64 characters of '0', '1', '2', '3', or '4', representing the germination status for each sowing position.
# The 64 characters start with the top left sowing position and continue row-wise.
# The score of every detection result is automatically calculated and displayed in the LCD number of a green background.
# Therefore, the audience can see the detection result in real time.
# The last detection score before the 5-min timer is up is the final detection score.
# The canvas displays the random germination statuses with squares and the detection result with circles.
# The color code is specified on the right. Note that black means that the server has not received a message from the robot.
# Author: Yin Bao, Auburn University, Biosystems Engineering Department

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QLineEdit, QLCDNumber, QComboBox, QLabel
import numpy as np
import socket
import threading
import time

NAME_IP_LIST = []
#Change the names and IP addresses of your robots in the list.
#They will be populated in the drop down manual
NAME_IP_LIST.append(['robot1','127.0.0.1'])
NAME_IP_LIST.append(['robot2','192.168.0.2'])
PORT = 50007

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.newDetectionAvailable = False
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.dropdown_menu = QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.dropdown_menu.setFont(font)
        self.dropdown_menu.setGeometry(QtCore.QRect(540, 540, 240, 50))
        self.robot_index = 0
        for name_ip in NAME_IP_LIST: 
            text = name_ip[0] + ': ' + name_ip[1]
            self.dropdown_menu.addItem(text)
        self.ip_addr = NAME_IP_LIST[0][1]

        self.server_running = True
        self.server_thread = threading.Thread(target = self.server) 
        self.server_thread.start()

        font = QtGui.QFont()
        font.setPointSize(20)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 800, 431))
        self.graphicsView.setObjectName("graphicsView")
        self.StandardButton = QtWidgets.QPushButton(self.centralwidget)
        self.StandardButton.setGeometry(QtCore.QRect(60, 470, 170, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StandardButton.sizePolicy().hasHeightForWidth())
        self.StandardButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.StandardButton.setFont(font)
        self.StandardButton.setObjectName("StandardButton")
        self.AdvancedButton = QtWidgets.QPushButton(self.centralwidget)
        self.AdvancedButton.setGeometry(QtCore.QRect(570, 470, 170, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.AdvancedButton.setFont(font)
        self.AdvancedButton.setObjectName("AdvancedButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.LCD = QLCDNumber(self.centralwidget)
        self.LCD.setGeometry(QtCore.QRect(350, 480, 100, 40))
        self.LCD.display(0)
        self.LCD.setStyleSheet('QLCDNumber {background-color: green; color: red;}')           
        
        self.clockLCD = QLCDNumber(self.centralwidget)
        self.clockLCD.setGeometry(QtCore.QRect(350, 540, 100, 40))
        self.clockLCD.display('3:00')
        self.clockLCD.setStyleSheet('QLCDNumber {background-color: yellow; color: red;}')

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        greenBrush = QBrush(Qt.green)   #2 single healthy
        yellowBrush = QBrush(Qt.yellow) #1 single stressed
        whiteBrush = QBrush(Qt.white)   #0 empty
        blueBrush = QBrush(Qt.blue)     #3 double
        pinkBrush = QBrush(Qt.magenta)  #4 tiller
        self.blackPen = QPen(Qt.black)
        self.BrushList = [whiteBrush, yellowBrush, greenBrush, blueBrush, pinkBrush, QBrush(Qt.black)]
        self.colorNames = ['Empty', 'Stressed', 'Healthy', 'Double','Tiller','Detection']
        
        self.level = 0 #standard
        self.newDetectionAvailable = False
        self.detectedFieldConfig = 5*np.ones((4,16),dtype=np.int8)
        self.fieldConfig = self.randFieldConfig()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.AdvancedButton.clicked.connect(self.AdvBtnClickedSlot)
        self.StandardButton.clicked.connect(self.StdBtnClickedSlot)
        self.StdBtnClickedSlot()
        self.drawPlants()
   
        self.drawing_timer = QTimer()
        self.drawing_timer.setInterval(50)
        self.drawing_timer.timeout.connect(self.updateDetectionResult)
        self.drawing_timer.start()

        self.clock_seconds = 0
        self.timestamp = '0:00'
        self.clock_timer = QTimer()
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self.updateClock)
        self.clock_timer.start()
        self.time_is_up = False
        app.aboutToQuit.connect(self.closeEvent)
    
    def updateClock(self):     
        if self.clock_seconds >= 300:      
            if self.clock_seconds%2 == 0:   
                self.clockLCD.setStyleSheet('QLCDNumber {background-color: yellow; color: red;}')
            else:
                self.clockLCD.setStyleSheet('QLCDNumber {background-color: white; color: red;}')
            self.clockLCD.display('5:00')
            self.time_is_up = True
        else:
            self.timestamp = str(self.clock_seconds//60)+':' 
            sec = self.clock_seconds%60
            self.timestamp += '0' + str(sec) if sec <10 else str(sec)
            self.clockLCD.display(self.timestamp)  
        self.clock_seconds += 1
        
    def updateDetectionResult(self):
       if self.newDetectionAvailable:
            self.drawPlants()
            self.newDetectionAvailable = False

    def closeEvent(self):
        self.server_running = False
        self.server_thread.join()

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', PORT))
            while self.server_running:
                try:
                    s.settimeout(1)
                    s.listen(1)
                    c, addr = s.accept() 
                    if addr[0] != self.ip_addr:
                        c.close()
                        continue
                    with c:  
                        while self.server_running:
                            try:       
                                c.settimeout(5)          
                                msg = c.recv(1024)
                                if len(msg) != 64:
                                    c.close()
                                    print('invalid msg')
                                    break
                                if not self.time_is_up:
                                    text = msg.decode('utf-8') 
                                    self.detectedFieldConfig = np.reshape(np.array(list(text),dtype=np.int8), (4,16))
                                    upper_limit = 3 if self.level == 0 else 5
                                    self.detectedFieldConfig[(self.detectedFieldConfig<0)|(self.detectedFieldConfig>=upper_limit)] = 5
                                    self.newDetectionAvailable = True
                                    #f = open("log.txt", "a")
                                    #f.write(self.ip_addr+','+self.timestamp+','+msg)
                                    #f.close()
                            except socket.timeout:
                                print('client stopped sending updates')
                                c.close()
                                break
                            except socket.error as exc:
                                print(exc)
                                c.close()
                                break
                except socket.timeout:
                    pass
            s.close()

    def drawPlants(self):
        size = 20
        hor_space = 40
        ver_space = 100
        self.scene.clear()
        for y in range(4):
            for x in range(16):
                plant_type = self.fieldConfig.item((y,x))
                r = QtCore.QRectF(QtCore.QPointF(x*hor_space, y*ver_space), QtCore.QSizeF(size, size))
                self.scene.addRect(r, self.blackPen, self.BrushList[plant_type])
                detected_plant_type = self.detectedFieldConfig.item((y,x))
                self.scene.addEllipse(x*hor_space, y*ver_space+30,size,size, self.blackPen, self.BrushList[detected_plant_type])
   
        # separation line
        self.scene.addLine(QtCore.QLineF(16.4*hor_space, 0, 16.4*hor_space, 350))
        # draw a legend
        for i in range(3 if self.level == 0 else 5):
            r = QtCore.QRectF(QtCore.QPointF(17*hor_space, i*ver_space/2), QtCore.QSizeF(size, size))
            self.scene.addRect(r, self.blackPen, self.BrushList[i])
            t = self.scene.addText(self.colorNames[i], QFont("Helvetica"))
            t.setPos(18*hor_space, i*ver_space/2)
        i = 3 if self.level==0 else 5
        self.scene.addEllipse(17*hor_space, i*ver_space/2, size, size, self.blackPen, self.BrushList[5])
        t = self.scene.addText(self.colorNames[5], QFont("Helvetica"))
        t.setPos(18*hor_space, i*ver_space/2)

        #calculate the score
        true_count_per_row = np.count_nonzero(np.logical_and(self.fieldConfig>0, self.fieldConfig<5),axis=1)+np.count_nonzero(self.fieldConfig==3, axis=1)
        robot_count_per_row = np.count_nonzero(np.logical_and(self.detectedFieldConfig>0, self.detectedFieldConfig<5),axis=1)+np.count_nonzero(self.detectedFieldConfig==3, axis=1)
        # plant density score
        error_per_row = np.abs(true_count_per_row-robot_count_per_row)
        density_score = np.zeros(4,dtype=np.int32)
        density_score[error_per_row==0] = 5
        density_score[error_per_row==1] = 3
        density_score[error_per_row==2] = 1
        correct_detections = self.fieldConfig[np.equal(self.fieldConfig, self.detectedFieldConfig)]
        points_for_empty_or_stress = 3 if self.level==0 else 2
        detection_score = points_for_empty_or_stress*len(correct_detections[(correct_detections==0)|(correct_detections==1)])
        
        if self.level==1:
            detection_score += 4*len(correct_detections[(correct_detections==3)|(correct_detections==4)])
        
        print(detection_score,density_score.sum())
        score = detection_score + density_score.sum()
        self.LCD.display(score)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "2020 ASABE Robotics Competition"))
        self.StandardButton.setText(_translate("MainWindow", "Standard"))
        self.AdvancedButton.setText(_translate("MainWindow", "Advanced"))

    def initialize(self):
        self.fieldConfig = self.randFieldConfig()
        self.drawPlants()
        self.server_running = False
        self.server_thread.join()
        self.ip_addr = NAME_IP_LIST[self.dropdown_menu.currentIndex()][1]
        self.server_thread = threading.Thread(target = self.server)
        self.server_running = True
        self.server_thread.start()
        self.time_is_up = False
        self.clock_seconds = 0
        self.clockLCD.setStyleSheet('QLCDNumber {background-color: yellow; color: red;}') 
        
    def StdBtnClickedSlot(self):
        self.StandardButton.setStyleSheet("background-color: red")
        self.AdvancedButton.setStyleSheet("background-color: gray")
        self.level = 0
        self.initialize()
        
    def AdvBtnClickedSlot(self):
        self.AdvancedButton.setStyleSheet("background-color: red")
        self.StandardButton.setStyleSheet("background-color: gray")
        self.level = 1
        self.initialize()
        
    def randFieldConfig(self):
        #reset robot detection result
        self.detectedFieldConfig = 5*np.ones((4,16),dtype=np.int8)
        # standard
        # 0: empty, 12
        # 1: single stressed, 8
        # 2: single healthy, 44

        # advanced
        # 0: empty, 12
        # 1: single stressed, 8
        # 2: single healthuy, 36
        # 3: double, 4 
        # 4: tiller, 4
        num_single_healthy_plants_per_row = 11 if self.level == 0 else 9
        single_healthy_block = 2*np.ones((4, num_single_healthy_plants_per_row), dtype=np.int8)
        num_abnormal_spots = 20 if self.level == 0 else 28
        abnormal_spots_array = np.zeros((1, num_abnormal_spots), dtype=np.int8)
        abnormal_spots_array[0,12:20] = 1
        if self.level == 1:
            abnormal_spots_array[0,20:24] = 3
            abnormal_spots_array[0,24:28] = 4
        shuffle_by_row = np.vectorize(np.random.permutation, signature='(n)->(n)')
        abnormal_spots_array = shuffle_by_row(abnormal_spots_array)
        abnormal_block = np.reshape(abnormal_spots_array,(4, -1))       
        fieldConfig = np.concatenate((single_healthy_block, abnormal_block), axis=1)
        fieldConfig = shuffle_by_row(fieldConfig) 
        return fieldConfig
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.randFieldConfig()
    MainWindow.show()
    sys.exit(app.exec_())

