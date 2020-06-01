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

            except Exception as e:
                print(e)
                robot.drive(0)

    def __init__(self,commAR,commDR,robot):
        self.angle = commAR
        self.distance = commDR
        self.robot = robot
