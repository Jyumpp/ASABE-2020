from LineTracing.lineTracing import lineTracing
import multiprocessing as mp
import threading
import time
from Robot.Robot import *

class LineCorrection:
    angle = None
    error = .5
    centerDistance = 0
    halt = True
    robot = None

    def checkAngle(self):
        while True:
            self.angle = self.pipeAngleR.recv()
            self.centerDistance = self.pipeDistanceR.recv()


    def whatMove(self,robot):
        checkThread = threading.Thread(target=self.checkAngle)
        checkThread.setdeamon = True
        checkThread.start()
        time.sleep(5)
        while True:
            try:
                if self.angle is None or self.centerDistance is None:
                    # print("None")
                    continue
                else:
                    if self.centerDistance > .5:
                        robot.drive(0)
                        robot.translate(90,-self.centerDistance/2)
                    elif self.centerDistance < -.5:
                        robot.drive(0)
                        robot.translate(90,abs(self.centerDistance)/2)
                    print(self.angle)
                    if self.angle < abs(self.error) and self.angle > -abs(self.error):
                        robot.drive(512)
                    elif self.angle > self.error:
                        robot.drive(0)
                        robot.centerAxis(-self.angle*.5)
                    elif self.angle < -self.error:
                        robot.drive(0)
                        robot.centerAxis(abs(self.angle)*.5)
                    time.sleep(.5)
            except Exception as e:
                print(e)
                robot.drive(0)


    def __init__(self,commAR,commDR):
        self.pipeAngleR = commAR
        self.pipeDistanceR = commDR
