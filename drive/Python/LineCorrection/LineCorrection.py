import multiprocessing as mp
import time
import math

class LineCorrection:
    errorAngle = .5
    errorDistance = .5
    robot = None

    def __init__(self,commAR,commDR,robot):
        self.angle = commAR
        self.distance = commDR
        self.robot = robot

    def whatMove(self,robot):
        time.sleep(5)
        while True:
            correctAngle = 0
            correctDistance = 0
            try:
                print(self.angle.value)
                #____________________________________Angle Correction______________________________#
                if abs(self.angle.value) > self.errorAngle:
                    if self.angle.value > self.errorAngle:
                        self.robot.centerAxis(-self.angle.value)
                    else:
                        self.robot.centerAxis(abs(self.angle.value))
                else:
                    print(self.distance.value)
                    #___________________________________Offset Correction______________________________#
                    #Detirmines if correction is needed
                    if self.distance.value > self.errorDistance:
                        correctAngle = -math.degrees(math.atan(self.distance.value))
                        correctDistance = ((self.distance.value ** 2) + 1) ** .5
                    elif self.distance.value < -self.errorDistance:
                        correctAngle = -math.degrees(math.atan(self.distance.value))
                        correctDistance = ((self.distance.value ** 2) + 1) ** .5
                    else:
                        correctAngle = 0
                        correctDistance = 0
                # Corrects path if needed otherwise continues forward
                if correctAngle == 0 and correctDistance == 0:
                    self.robot.drive(512)
                else:
                    self.robot.translate(correctAngle,correctDistance)
            except Exception as e:
                print("Error")
                print(e)
            time.sleep(.25)
