import multiprocessing as mp
import time
import math

class LineCorrection:
    error = .5
    robot = None

    def __init__(self,commAR,commDR,robot):
        self.angle = commAR
        self.distance = commDR
        self.robot = robot

    def whatMove(self,robot):
        time.sleep(5)
        while True:
            try:
                #____________________________________Angle Correction______________________________#
                # tan(angle)*18.0625
                #print(self.angle.value)
                if self.angle.value > self.error:
                    self.robot.centerAxis(-self.angle.value)
                elif self.angle.value < -self.error:
                    self.robot.centerAxis(abs(self.angle.value))
                else:
                    #___________________________________Offset Correction______________________________#
                    #Detirmines if correction is needed
                    if abs(self.distance.value) > self.error:
                        correctAngle = math.atan(self.distance.value/2)
                        correctDistance = ((self.distance.value ** 2) + 4) ** .5
                    else:
                        correctAngle = 0
                        correctDistance = 0
                        # Corrects path if needed otherwise continues forward
                    if correctAngle == 0 and correctDistance == 0:
                        self.robot.drive(512)
                    else:
                        self.robot.translate(correctAngle,correctDistance)
            except Exception as e:
                print("Shits not working")
                print(e)
