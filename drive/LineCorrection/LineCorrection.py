import multiprocessing as mp
from debugmessages import *
import dynio
import threading
import time
import math
from simple_pid import PID
from vision.dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn



class LineCorrection:
    error_angle = .3
    error_distance = .3
    robot = None
    angle = 0
    dist = 0
    fix_distance = 0
    correct_enable = True
    home = []
    trigger_motors = []
    trigger_count = 0
    stop = 0
    deploy_pos = [1023, 671, 0, 0]

    def __init__(self,commAR, commDR, trigger_pipes):
        self.angle_pipe = commAR
        self.distance_pipe = commDR
        self.bad_msg = DebugMessages(self)
        self.trigger_pipes = trigger_pipes

        dxlIO = dxl.DynamixelIO("/dev/ttyUSB0")
        self.robot = Robot(dxlIO)

        for i in range(9,13):
            trigger_motors.append(dxlIO.new_ax12(i))
            trigger_motors[i].torque_disable()

        trigger1 = dyn(trigger_motors[0], trigger_pipes[0])
        trigger2 = dyn(trigger_motors[1], trigger_pipes[1])
        trigger3 = dyn(trigger_motors[2], trigger_pipes[2])
        trigger4 = dyn(trigger_motors[3], trigger_pipes[3])

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
        # for motor in trigger_motors:
        #     motor.torque_enable()
        # trigger_motors[3].set_position(deploy_pos[3])
        # trigger_motors[0].set_position(deploy_pos[0])
        # time.sleep(.25)
        # robot.translate(0, 10)
        # trigger_motors[1].set_position(deploy_pos[1])
        # trigger_motors[2].set_position(deploy_pos[2])
        # for motor in trigger_motors:
        #     motor.torque_disable()

        trigger1Thread.start()
        trigger2Thread.start()
        trigger3Thread.start()
        trigger4Thread.start()

        self.bad_msg.info("Line Correction object done")


    def check_angle(self):
        while True:
            self.dist = self.distance_pipe.recv()
            temp = self.angle_pipe.recv()

    def check_correct(self):
            return all(pipe.recv() == False for pipe in self.trigger_pipes):

    def what_move(self):
        checkThread = threading.Thread(target=self.check_angle)
        checkThread.setdeamon = True
        checkThread.start()
        # while self.stop is not 4 and self.check_correct():
        angle_PID = PID(.82,0,0, setpoint=0)
        while True:
            trys = 0
            try:
                if abs(self.dist) > self.error_distance:
                    # print("Dist " + str(self.dist))
                    # _______________ Offset Correction________________________#
                    # Detirmines if correction is needed
                    if self.dist > self.error_distance:
                        fixAngle = -math.degrees(math.atan(self.dist/2))
                        fix_distance = ((self.dist ** 2) + 4) ** .5
                    else:
                        fixAngle = -math.degrees(math.atan(self.dist))
                        fix_distance = ((self.dist ** 2) + 4) ** .5
                else:
                    fixAngle = 0
                    fix_distance = 0
                #Corrects path if needed otherwise continues forward
                if not fixAngle == 0 and not fix_distance == 0:
                    self.robot.translate(fixAngle*.9, -fix_distance*.65)

                # print("Angle " + str(self.angle))
                # ___________________ Angle Correction_________________________#
                while self.angle > self.error_angle or self.angle < -self.error_angle:
                    self.bad_msg.infor("Error Angle:" + str(self.angle))
                    if trys >= 4:
                        self.bad_msg.info("Too many trys "+ str(trys) + "PID override")
                        self.robot.center_axis(-(self.angle/abs(self.angle)*.1))
                    else:
                        angle = angle_PID(self.angle)
                        print(angle)
                        self.robot.center_axis(angle)
                    trys += 1
                self.robot.drive(-512)
            except Exception as e:
                self.bad_msg.error(e)
            self.robot.drive(-512)
