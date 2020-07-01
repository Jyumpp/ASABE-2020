import time
import math
import queue
import threading
import multiprocessing as mp
from dynio import *
from debugmessages import *
from simple_pid import PID
from drive.Robot.Motor import *
from drive.Robot.Robot import *
from drive.LineTracing.lineTracing import *
from vision.dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn
import copy


class LineCorrection:
    error_angle = .3
    error_distance = .3
    robot = None
    angle = 0
    dist = 0
    fix_distance = 0
    correct_enable = True
    home = []
    trigger_count = 0
    stop = 0


    def __init__(self,commAR, commDR, trigger_pipes):

        self.bad_msg = DebugMessages(self)
        self.bad_msg.info("Beginning Line Correction initialization")
        self.angle_pipe = commAR
        self.distance_pipe = commDR
        self.trigger_pipes = trigger_pipes
        self.trigger_motors = []
        self.deploy_pos = [1003, 637, 9, 9]

        self.dxlIO = dxl.DynamixelIO("/dev/ttyUSB0")
        self.lock = self.dxlIO.lock
        with self.lock:
            self.robot = Robot(self.dxlIO)

        self.bad_msg.info("Line Correction object done")


    def check_angle(self):
        while True:
            self.dist = self.distance_pipe.recv()
            self.angle = self.angle_pipe.recv()

    def what_move(self):
        self.bad_msg.info("What Move started")
        checkThread = threading.Thread(target=self.check_angle)
        checkThread.setdeamon = True
        checkThread.start()

        self.bad_msg.info("Creating Dropper Trigger motors")

        for i in range(9,13):
            self.trigger_motors.append(self.dxlIO.new_ax12(i))
            self.trigger_motors[i-9].torque_disable()

        self.bad_msg.info("Starting expandy_boi and Trigger Dropper deployment")
        # # Running expandy boi
        # robot.expandy_boi()
        # self.robot.translate(0, -8)
        self.trigger_motors[3].set_position(self.deploy_pos[3])
        self.trigger_motors[0].set_position(self.deploy_pos[0])
        # time.sleep(.25)
        # self.robot.translate(0, 8)
        self.trigger_motors[1].set_position(self.deploy_pos[1])
        self.trigger_motors[2].set_position(self.deploy_pos[2])
        # for motor in trigger_motors:
        #     motor.torque_disable()
        self.bad_msg.info("Finished expandy_boi and trigger dropper deployment")

        self.bad_msg.info("Creating Trigger classes")
        trigger1 = dyn(self.trigger_motors[0], self.deploy_pos[0], self.trigger_pipes[0])
        trigger2 = dyn(self.trigger_motors[1], self.deploy_pos[1], self.trigger_pipes[1])
        trigger3 = dyn(self.trigger_motors[2], self.deploy_pos[2], self.trigger_pipes[2])
        trigger4 = dyn(self.trigger_motors[3], self.deploy_pos[3], self.trigger_pipes[3])

        self.bad_msg.info("Creating Trigger Threads")
        trigger1Thread = threading.Thread(target=trigger1.Run, args=())
        trigger1Thread.daemon = True
        trigger2Thread = threading.Thread(target=trigger2.Run, args=())
        trigger2Thread.daemon = True
        trigger3Thread = threading.Thread(target=trigger3.Run, args=())
        trigger3Thread.daemon = True
        trigger4Thread = threading.Thread(target=trigger4.Run, args=())
        trigger4Thread.daemon = True

        self.bad_msg.info("Beginning Trigger threads.")

        trigger1Thread.start()
        trigger2Thread.start()
        trigger3Thread.start()
        trigger4Thread.start()

        # Position Cameras


        time.sleep(.7)
        # while self.stop is not 4 and all(pipe.recv() == False for pipe in self.trigger_pipes):
        angle_PID = PID(.82,0,0, setpoint=0)
        # self.dxlIO2.manual_threading[1]=True
        while True:
            time.sleep(.3)
            trys = 0
            try:
                # print("Angle " + str(self.angle))
                # ___________________ Angle Correction_________________________#
                while self.angle > self.error_angle or self.angle < -self.error_angle:
                    self.bad_msg.info("Error Angle:" + str(self.angle))
                    if trys >= 4:
                        self.bad_msg.info("Too many trys "+ str(trys) + " PID override")
                        with self.lock:
                            self.robot.center_axis(-(self.angle/abs(self.angle)*.1))
                        break
                    else:
                        angle = angle_PID(self.angle)
                        print(angle)
                        with self.lock:
                            self.robot.center_axis(angle)
                    trys += 1

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
                    with self.lock:
                        self.robot.translate(fixAngle*.9, -fix_distance*.65)
                else:
                    with self.lock:
                        self.robot.drive(-256)

            except Exception as e:
                self.bad_msg.error(e)

        # if all rows done return
        with self.lock:
            self.robot.drive(0)
