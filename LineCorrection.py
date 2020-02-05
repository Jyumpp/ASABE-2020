from lineTracing import lineTracking
from dynio import dynamixel_controller as dyn
import threading
import time

class LineCorrection:
    test = lineTracking()
    motor = []
    d = dyn.DynamixelIO(device_name="/dev/ttyUSB0")
    angle = None
    error = 1


    def stop(self):
         for motors in self.motor:
             motors.set_velocity(0)

    def turnLeft(self,velocity):
        #self.motor[0].set_velocity(-velocity)
        self.motor[1].set_velocity(-velocity)
        #self.motor[2].set_velocity(-velocity)
        self.motor[3].set_velocity(-velocity)

    def turnRight(self,velocity):
        #self.motor[0].set_velocity(velocity)
        self.motor[1].set_velocity(velocity)
        #self.motor[2].set_velocity(velocity)
        self.motor[3].set_velocity(velocity)

    def forward(self,velocity):
        self.motor[0].set_velocity(velocity)
        self.motor[1].set_velocity(velocity)
        self.motor[2].set_velocity(-velocity)
        self.motor[3].set_velocity(-velocity)

    def otherForward(self,velocity):
        self.stop()
        self.forward(-velocity)

    def checkAngle(self):
        while True:
            self.angle =  self.test.getAngle()

    def whatMove(self):
        time.sleep(5)
        while True:
            print(self.angle)
            try:
                if self.angle > self.error:
                    self.stop()
                    self.turnLeft(25)
                elif self.angle < -self.error:
                    self.stop()
                    self.turnRight(25)
                elif self.error > self.angle and self.angle > -self.error:
                    self.forward(50)
                else:
                    self.stop()
            except:
                self.stop()

    def __init__(self):
        init = True
        while init:
            try:
                for motors in range(0,4):
                    self.motor.append(self.d.new_mx12_1(motors + 1))
                    self.motor[motors].set_velocity_mode()
                    self.motor[motors].torque_enable()
                init = False
            except:
                print("Plug in motors")
                time.sleep(5)

        angleThread = threading.Thread(target=self.checkAngle)
        angleThread.setdaemon = True
        angleThread.start()


        functionThread = threading.Thread(target=self.whatMove)
        functionThread.setdeamon = True
        functionThread.start()

lineCorrection = LineCorrection()
