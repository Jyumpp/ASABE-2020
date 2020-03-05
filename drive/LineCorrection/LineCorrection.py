from LineTracing.lineTracing import lineTracing
import multiprocessing as mp
import threading
import time
from Robot.Robot import *

class LineCorrection:
    angle = None
    error = 1
    centerDistacne = 0
    halt = True
    robot = None
    pipeAngleR = None
    pipeDistanceR = None

    def checkAngle(self):
      self.angle = self.pipeAngleR.recv()
      self.centerDistance = self.pipeDistanceR.recv()


    def whatMove(self):
        print("Start")
        time.sleep(2)
        checkThread = threading.Thread(target=self.checkAngle)
        checkThread.setdeamon = True
        checkThread.start()
        time.sleep(5)
        while True:
            try:
                if self.centerDistance > .5:
                    self.halt = True
                    self.robot.drive(0)
                    self.robot.translate(90,-self.centerDistance/2)
                elif self.centerDistance < -.5:
                    self.halt = True
                    self.robot.drive(0)
                    self.robot.translate(90,abs(self.centerDistance)/2)
                print(self.angle)
                if self.angle < abs(self.error) and self.angle > -abs(self.error):
                    self.robot.drive(512)
                    self.halt = False
                elif self.angle > self.error:
                    self.halt = True
                    self.robot.drive(0)
                    self.robot.centerAxis(-self.angle)
                    self.halt = False
                elif self.angle < -self.error:
                    self.halt = True
                    self.robot.drive(0)
                    self.robot.centerAxis(abs(self.angle))
                    self.halt = False
                time.sleep(.5)
            except Exception as e:
                print(e)
                self.halt = False
                self.robot.drive(0)


    def __init__(self,commAR,commDR):
        self.pipeAngleR = commAR
        self.pipeDistanceR = commDR
        self.robot = Robot("/dev/ttyUSB0")
        #self.robot.expandyBoi()
        #self.robot.drive(512)
        #time.sleep(.5)
        #self.robot.drive(0)
        # if __name__ == '__main__':
        #     pipeR,pipeW = mp.Pipe()
        #     l = lineTracing(pipeR,pipeW)
        #     mp.set_start_method('spawn')
        #     thread = mp.Process(target=l.lineTracer, args=())
        #     thread.start()
        #
        # # angleThread = threading.Thread(target=self.checkAngle)
        # # angleThread.setdaemon = True
        # # angleThread.start()
        # #self.robot.translate(90,43)
        # functionThread = threading.Thread(target=self.whatMove)
        # functionThread.setdeamon = True
        # functionThread.start()
        # time.sleep(5)

# lineCorrection = LineCorrection()
