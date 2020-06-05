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
                if abs(self.angle.value) > self.error or abs(self.distance.value) > self.error:
                    if self.angle.value > 0:
                        print("> 0" + str(self.distance.value))
                        correctionAngle = -self.angle.value - math.degrees(math.atan(self.distance.value/2))
                    elif self.angle == 0:
                        correctionAngle = math.degrees(math.atan(self.distance.value/2))
                    else:
                        print("< 0" + str(self.distance.value))
                        correctionAngle = abs(self.angle.value) - math.degrees(math.atan(self.distance.value/2))
                    print(correctionAngle)
                    self.robot.centerAxis(correctionAngle)
                self.robot.drive(512)
                # else:
                    # #___________________________________Offset Correction______________________________#
                    # #Detirmines if correction is needed
                    # if abs(self.distance.value) > self.error:
                    #     correctAngle = math.atan(self.distance.value/2)
                    #     correctDistance = ((self.distance.value ** 2) + 4) ** .5
                    # else:
                    #     correctAngle = 0
                    #     correctDistance = 0
                    #     # Corrects path if needed otherwise continues forward
                    # if correctAngle == 0 and correctDistance == 0:
                    #     self.robot.drive(512)
                    # else:
                    #     self.robot.translate(correctAngle,correctDistance)
            except Exception as e:
                print("Shits not working")
                print(e)
            time.sleep(1)
