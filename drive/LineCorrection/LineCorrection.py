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

    def __init__(self, commAR, commDR, robot):
        self.anglePipe = commAR
        self.distancePipe = commDR
        self.robot = robot
        self.badMsg = DebugMessages(self)
        self.badMsg.info("Line Correction object done")
        # self.stopFlag = stopFlag

    def check_angle(self):
        while True:
            self.dist = self.distancePipe.recv()
            temp = self.anglePipe.recv()

    def what_move(self):
        checkThread = threading.Thread(target=self.check_angle)
        checkThread.setdeamon = True
        checkThread.start()
        # while self.stopFlag.value is not 4:
        anglePID = PID(.82,0,0, setpoint=0)
        while True:
            trys = 0
            try:
                # print("Angle " + str(self.angle))
                # ___________________ Angle Correction_________________________#
                while self.angle > self.errorAngle or self.angle < -self.errorAngle:
                    print("Error Angle:" + str(self.angle))
                    print("Trys" + str(trys))
                    if trys > 4:
                        print("too many trys")
                        self.robot.center_axis(-(self.angle/abs(self.angle)*.1))
                    else:
                        angle = anglePID(self.angle)
                        print(angle)
                        self.robot.center_axis(angle)
                    trys += 1
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
                if fixAngle == 0 and fixDistance == 0:
                    self.robot.drive(-512)
                else:
                    self.robot.translate(fixAngle*.9, -fixDistance*.65)
            except Exception as e:
                print(e)
                self.badMsg.error(e)
