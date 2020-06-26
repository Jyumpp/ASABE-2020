from dynio import *
from debugmessages import *


class Motor:
    count = 1
    dyn = None
    badMsg = None

    def __init__(self, side, dyn):

        self.badMsg = DebugMessages(self)

        if Motor.dyn is None:
            Motor.dyn = dyn
            
        self.badMsg.info(str(Motor.count))
        # creates the motor to control the wheel angle
        self.angleMotor = Motor.dyn.new_ax12(Motor.count)

        # sets the motor torque limit and position mode
        self.angleMotor.set_position_mode(goal_current=512)
        self.angleMotor.torque_enable()
        self.torque = True

        # increments the motor ID
        Motor.count = Motor.count + 1

        self.badMsg.info(str(Motor.count))

        # creates the motor that controls wheel velocity
        self.driveMotor = Motor.dyn.new_ax12(Motor.count)
        self.driveMotor.set_velocity_mode()
        self.driveMotor.torque_enable()
        Motor.count = Motor.count + 1

        # Tracks the side of the Robot the Motor is on
        self.right = side
        self.homeAngle = 150

    # Toogles torque for the drive motor
    def toggle_Torque(self):
        if self.driveMotor.read_control_table("Torque_Enable") == 1:
            self.driveMotor.torque_disable()
        else:
            self.driveMotor.torque_enable()

    # Gets the current angle of the motor
    def get_angle(self):
        return self.angleMotor.get_angle()

    # Sets the angle of the motor
    def set_angle(self, angle):
        self.angleMotor.set_angle(self.homeAngle - angle)

    # Sets the motor to home angle
    def center(self):
        self.angleMotor.set_angle(self.homeAngle)

    # Sets the wheel velocity
    def set_velocity(self, velocity):
        if self.right:
            self.driveMotor.set_velocity(-velocity)
        else:
            self.driveMotor.set_velocity(velocity)

    def get_velocity(self):
        return driveMotor.read_control_table("Present_Speed")
