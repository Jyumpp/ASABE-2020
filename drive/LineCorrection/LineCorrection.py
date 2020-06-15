import multiprocessing as mp
import time
import math


class LineCorrection:
    errorAngle = .5
    errorDistance = .5
    robot = None

    def __init__(self, commAR, commDR, robot):
        self.angle = commAR
        self.dist = commDR
        self.robot = robot

    def what_move(self, robot):
        time.sleep(5)
        while True:
            fixAngle = 0
            fixDistance = 0
            try:
                print(self.angle.value)
                # ___________________Angle Correction_________________________#
                if abs(self.angle.value) > self.errorAngle:
                    if self.angle.value > self.errorAngle:
                        self.robot.center_axis(-self.angle.value)
                    else:
                        self.robot.center_axis(abs(self.angle.value))
                else:
                    print(self.dist.value)
                    # _______________Offset Correction________________________#
                    # Detirmines if correction is needed
                    if self.dist.value > self.errorDistance:
                        fixAngle = -math.degrees(math.atan(self.dist.value))
                        fixDistance = ((self.dist.value ** 2) + 1) ** .5
                    elif self.dist.value < -self.errorDistance:
                        fixAngle = -math.degrees(math.atan(self.dist.value))
                        fixDistance = ((self.dist.value ** 2) + 1) ** .5
                    else:
                        fixAngle = 0
                        fixDistance = 0
                # Corrects path if needed otherwise continues forward
                if fixAngle == 0 and fixDistance == 0:
                    self.robot.drive(512)
                else:
                    self.robot.translate(fixAngle, fixDistance)
            except Exception as e:
                print("Error")
                print(e)
            time.sleep(.25)
