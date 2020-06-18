import multiprocessing as mp
from debugmessages import *
import threading
import time
import math


class LineCorrection:
    errorAngle = .25
    errorDistance = .5
    robot = None
    angle = 0
    dist = 0
    fixDistance = 0
    fixAngle = 0

    def __init__(self, stopFlag, commAR, commDR, robot):
        self.angleQueue.get()Queue = commAR
        self.distanceQueue = commDR
        self.robot = robot
        self.badMsg = DebugMessages(self)
        self.badMsg.info("Line Correction object done")
        self.stopFlag = stopFlag

    def what_move(self):
        time.sleep(5)
        self.robot.expandy_boi()
        while self.stopFlag.value is not 4:
            try:
                print("Angle " + str(self.angleQueue.get()))

                # ___________________Angle Correction_________________________#
                if abs(self.angleQueue.get()) > self.errorAngle:
                    if self.angleQueue.get() > self.errorAngle:
                        self.robot.center_axis(-self.angleQueue.get())
                    else:
                        self.robot.center_axis(abs(self.angleQueue.get()))
                if abs(self.distanceQueue.get()) > self.errorDistance:
                    print("Dist " + str(self.distanceQueue.get()))

                    # _______________Offset Correction________________________#
                    # Detirmines if correction is needed
                    if self.distanceQueue.get() > self.errorDistance:
                        fixAngle = -math.degrees(math.atan(self.distanceQueue.get() / 2))
                        fixDistance = ((self.distanceQueue.get() ** 2) + 4) ** .5
                    else:
                        fixAngle = -math.degrees(math.atan(self.distanceQueue.get()))
                        fixDistance = ((self.distanceQueue.get() ** 2) + 4) ** .5
                else:
                    fixAngle = 0
                    fixDistance = 0

                # Corrects path if needed otherwise continues forward
                if fixAngle == 0 and fixDistance == 0:
                    self.robot.drive(512)
                else:
                    self.robot.translate(fixAngle * .9, fixDistance * .65)

            # Stops the robot at the end of the run
            robot.drive(0)
            robot.center(0)
            except Exception as e:
                print(e)
                self.badMsg.error(e)
