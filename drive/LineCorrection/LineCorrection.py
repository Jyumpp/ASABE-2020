import multiprocessing as mp
from debugmessages import *
import threading
import time
import math
from simple_pid import PID


class LineCorrection:
    errorAngle = .3
    errorDistance = .5
    robot = None
    angle = 0
    dist = 0
    fixDistance = 0
    fixAngle = 0

    def __init__(self, stopFlag,courseCorrect,commAR, commDR, robot):
        self.anglePipe = commAR
        self.distancePipe = commDR
        self.robot = robot
        self.badMsg = DebugMessages(self)
        self.badMsg.info("Line Correction object done")
        # self.stopFlag = stopFlag
        # self.courseCorrect = courseCorrect

    def check_angle(self):
        while True:
            self.dist = self.distancePipe.recv()
            temp = self.anglePipe.recv()

    def what_move(self):
        checkThread = threading.Thread(target=self.check_angle)
        checkThread.setdeamon = True
        checkThread.start()
        # while self.stopFlag.value is not 4 and self.courseCorrect.value == 0:
        anglePID = PID(.82,0,0, setpoint=0)
        while True:
            trys = 0
            try:
                if abs(self.dist) > self.errorDistance:
                    # print("Dist " + str(self.dist))
                    # _______________ Offset Correction________________________#
                    # Detirmines if correction is needed
                    if self.dist > self.errorDistance:
                        fixAngle = -math.degrees(math.atan(self.dist/2))
                        fixDistance = ((self.dist ** 2) + 4) ** .5
                    else:
                        fixAngle = -math.degrees(math.atan(self.dist))
                        fixDistance = ((self.dist ** 2) + 4) ** .5
                else:
                    fixAngle = 0
                    fixDistance = 0
                #Corrects path if needed otherwise continues forward
                if not fixAngle == 0 and not fixDistance == 0:
                    self.robot.translate(fixAngle*.9, -fixDistance*.65)

                # print("Angle " + str(self.angle))
                # ___________________ Angle Correction_________________________#
                while self.angle > self.errorAngle or self.angle < -self.errorAngle:
                    self.badMsg.infor("Error Angle:" + str(self.angle))
                    if trys >= 4:
                        self.badMsg.info("Too many trys "+ str(trys) + "PID override")
                        self.robot.center_axis(-(self.angle/abs(self.angle)*.1))
                    else:
                        angle = anglePID(self.angle)
                        print(angle)
                        self.robot.center_axis(angle)
                    trys += 1
                self.robot.drive(-512)
            except Exception as e:
                self.badMsg.error(e)
