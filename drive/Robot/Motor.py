import time
from dynio import *


class Motor:
    count = 1
    dyn = None
    def __init__(self, side, path):
        if Motor.dyn is None:
            # Creates DynamixelIO object
            Motor.dyn = dxl.DynamixelIO(device_name=path)
        # creates the motor to control the wheel angle
        self.angleMotor = dyn.new_ax12_1(Motor.count)
        # sets the motor torque limit and position mode
        self.angleMotor.set_position_mode(goal_current=512)
        self.angleMotor.torque_enable()
        self.torque = True
        # increments the motor ID
        Motor.count = Motor.count + 1
        # creates the motor that controls wheel velocity
        self.driveMotor = dyn.new_ax12_1(Motor.count)
        self.driveMotor.set_velocity_mode()
        self.driveMotor.torque_enable()
        Motor.count = Motor.count + 1
        self.right = side
        self.homeAngle = 150

    def getAngle(self):
        return self.angleMotor.get_angle()

    def setAngle(self,angle):
        self.angleMotor.set_angle(self.homeAngle - angle)

    # Sets the motor to home angle
    def center(self):
        self.angleMotor.set_angle(self.homeAngle)

    # Sets the wheel velocity
    def setVelocity(self,velocity):
        if self.right:
            self.driveMotor.set_velocity(-velocity)
        else:
            self.driveMotor.set_velocity(velocity)

    def getVelocity(self):
        return driveMotor.read_control_table("Present_Speed")
