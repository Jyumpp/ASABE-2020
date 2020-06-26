import multiprocessing as mp
from debugmessages import *
import dynio
import threading
import time
import math
from simple_pid import PID
from vision.dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn



class LineCorrection:
    errorAngle = .3
    errorDistance = .5
    robot = None
    angle = 0
    dist = 0
    fixDistance = 0
    correctEnable = True
    home = []
    triggerMotors = []
    triggerCount = 0
    stop = 0

    def __init__(self,courseCorrect,commAR, commDR, robot, triggerWrite1, triggerWrite2, triggerWrite3, triggerWrite4):
        self.anglePipe = commAR
        self.distancePipe = commDR
        self.badMsg = DebugMessages(self)

        dxlIO = dxl.DynamixelIO("/dev/ttyUSB0")
        self.robot = Robot(dxlIO)

        trigger1 = dyn(triggerMotors[0], triggerWrite1)
        trigger2 = dyn(triggerMotors[1], triggerWrite2)
        trigger3 = dyn(triggerMotors[2], triggerWrite3)
        trigger4 = dyn(triggerMotors[3], triggerWrite4)

        trigger1Thread = thread.Thread(target=trigger1.Run, args=())
        trigger1Thread.setDaemon = True
        trigger2Thread = thread.Thread(target=trigger2.Run, args=())
        trigger2Thread.setDaemon = True
        trigger3Thread = thread.Thread(target=trigger3.Run, args=())
        trigger3Thread.setDaemon = True
        trigger4Thread = thread.Thread(target=trigger4.Run, args=())
        trigger4Thread.setDaemon = True

        # # Running expandy boi
        # robot.expandy_boi()
        # robot.translate(0, -8)
        # for motor in motorList:
        #     motor.torque_enable()
        # motorList[3].set_position(deployAngles[3])
        # motorList[0].set_position(deployAngles[0])
        # time.sleep(.25)
        # robot.translate(0, 10)
        # motorList[1].set_position(deployAngles[1])
        # motorList[2].set_position(deployAngles[2])
        # for motor in motorList:
        #     motor.torque_disable()

        trigger1Thread.start()
        trigger2Thread.start()
        trigger3Thread.start()
        trigger4Thread.start()

        self.badMsg.info("Line Correction object done")




    def check_angle(self):
        while True:
            self.dist = self.distancePipe.recv()
            temp = self.anglePipe.recv()

    def check_correct(self):
        while True:
            if all(pipe.recv() == False for pipe in self.courseCorrect):
                self.correctEnable = False
            else:
                self.correctEnable = True

    def what_move(self):
        checkThread = threading.Thread(target=self.check_angle)
        checkThread.setdeamon = True
        checkThread.start()
        checkCorrectEnable = threading.Thread(target=self.check_correct)
        checkCorrectEnable.setDaemon = True
        checkCorrectEnable.start()
        # while self.stop is not 4 and self.correctEnable:
        anglePID = PID(.82,0,0, setpoint=0)
        while True:
            trys = 0
            try:
                if abs(self.dist) > self.errorDistance:
                    # print("Dist " + str(self.dist))
                    # _______________ Offset Correction________________________#
                    # Detirmines if correction is needed
                    if self.dist > self.errorDistance:
                        fixAngle = -math.degrees(math.atan(self.dist/2))
                        fixDistance = ((self.dist ** 2) + 4) ** .5
                    else:
                        fixAngle = -math.degrees(math.atan(self.dist))
                        fixDistance = ((self.dist ** 2) + 4) ** .5
                else:
                    fixAngle = 0
                    fixDistance = 0
                #Corrects path if needed otherwise continues forward
                if not fixAngle == 0 and not fixDistance == 0:
                    self.robot.translate(fixAngle*.9, -fixDistance*.65)

                # print("Angle " + str(self.angle))
                # ___________________ Angle Correction_________________________#
                while self.angle > self.errorAngle or self.angle < -self.errorAngle:
                    self.badMsg.infor("Error Angle:" + str(self.angle))
                    if trys >= 4:
                        self.badMsg.info("Too many trys "+ str(trys) + "PID override")
                        self.robot.center_axis(-(self.angle/abs(self.angle)*.1))
                    else:
                        angle = anglePID(self.angle)
                        print(angle)
                        self.robot.center_axis(angle)
                    trys += 1
                self.robot.drive(-512)
            except Exception as e:
                self.badMsg.error(e)
            self.robot.drive(-512)
