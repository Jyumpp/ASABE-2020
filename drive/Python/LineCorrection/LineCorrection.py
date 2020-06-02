<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import multiprocessing as mp
import time

class LineCorrection:
    error = .5
    robot = None

    def whatMove(self,robot):
        time.sleep(5)
        while True:
            try:
                #____________________________________Angle Correction______________________________#
                print(self.angle.value)
                if self.angle.value > self.error:
                    robot.drive(0)
                    robot.centerAxis(-self.angle.value*.5)
                elif self.angle < -self.error:
                    robot.drive(0)
                    robot.centerAxis(abs(self.angle.value)*.5)
                #___________________________________Offset Correction______________________________#
                #Detirmines if correction is needed
                if abs(self.distance.value) > .5:
                    angle = math.atan(self.distance.value/2)
                    distance = (self.distance.value**2 + 4) ** (1/2)
                else self.distance < -.5:
                    angle = 0
                # Corrects path if needed otherwise continues forward
                robot.dive(512) if (angle == 0 && distance == 0) else robot.translate(angle,distance)

                time.sleep(.5)

=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
            except Exception as e:
                print(e)
                robot.drive(0)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def __init__(self,commAR,commDR,robot):
        self.angle = commAR
        self.distance = commDR
        self.robot = robot
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    def __init__(self,commAR,commDR):
        self.pipeAngleR = commAR
        self.pipeDistanceR = commDR
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
