import multiprocessing as mp
from debugmessages import *
import threading
import time
import math


class LineCorrection:
    errorAngle = .5
    errorDistance = .25
    robot = None
    angle = 0
    dist = 0

    def __init__(self, commAR, commDR, robot):
        self.anglePipe = commAR
        self.distancePipe = commDR
        self.robot = robot
        #self.badMsg = DebugMessages(self)
        #self.badMsg.info("Line Correction object done")

    def check_angle(self):
        while True:
            self.dist = self.distancePipe.recv()
            self.angle = self.anglePipe.recv()

    def what_move(self):
        checkThread = threading.Thread(target=self.check_angle)
        checkThread.setdeamon = True
        checkThread.start()
        time.sleep(5)
        while True:
            fixAngle = 0
            fixDistance = 0
            try:
                print("Angle " + str(self.angle))
                # ___________________Angle Correction_________________________#
                if abs(self.angle) > self.errorAngle:
                    if self.angle > self.errorAngle:
                        self.robot.center_axis(-self.angle)
                    else:
                        self.robot.center_axis(abs(self.angle))
                else:
                    print("Dist " + str(self.dist))
                    # _______________Offset Correction________________________#
                    # Detirmines if correction is needed
                    if self.dist > self.errorDistance:
                        fixAngle = -math.degrees(math.atan(self.dist))
                        fixDistance = ((self.dist ** 2) + 1) ** .5
                    elif self.dist < -self.errorDistance:
                        fixAngle = -math.degrees(math.atan(self.dist))
                        fixDistance = ((self.dist ** 2) + 1) ** .5
                    else:
                        fixAngle = 0
                        fixDistance = 0
                #Corrects path if needed otherwise continues forward
                if fixAngle == 0 and fixDistance == 0:
                    self.robot.drive(512)
                else:
                    self.robot.translate(fixAngle, fixDistance)
            except Exception as e:
                print(e)
                #self.badMsg.error(e)
            time.sleep(1)
