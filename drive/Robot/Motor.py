from dynio import *
import time

class Motor:
    count = 1

    def __init__(self,side,path):
        dyn = dxl.DynamixelIO(device_name=path)
        self.angleMotor = dyn.new_ax12_1(Motor.count)
        self.angleMotor.set_position_mode(goal_current=512)
        self.angleMotor.torque_enable()
        self.torque = True
        Motor.count = Motor.count + 1
        self.driveMotor = dyn.new_ax12_1(Motor.count)
        self.driveMotor.set_velocity_mode()
        self.driveMotor.torque_enable()
        Motor.count = Motor.count + 1
        self.right = side
        self.homeAngle = 150

    def toggleAngle():
        if self.torque:
            self.angleMotor.torque_disable()
        else:
            self.angleMotor.torque_enable()
    def getAngle(self):
        return self.angleMotor.get_angle()

    def setAngle(self,angle):
        self.angleMotor.set_angle(self.homeAngle - angle)

    def center(self):
        self.angleMotor.set_angle(self.homeAngle)

    def stop(self):
        self.driveMotor.set_velocity(0)

    def setVelocity(self,velocity):
        if self.right:
            self.driveMotor.set_velocity(-velocity)
        else:
            self.driveMotor.set_velocity(velocity)

    def getVelocity(self):
        return driveMotor.read_control_table("Present_Speed")

    def getPosition(self):
        return self.driveMotor.get_position()
