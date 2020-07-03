from dynio import *
from debugmessages import *


class Motor:
    count = 1
    dxl_io = None
    bad_msg = None

    def __init__(self, side, dxl_io):

        self.bad_msg = DebugMessages(self)

        if Motor.dxl_io is None:
            Motor.dxl_io = dxl_io

        # self.bad_msg.info("Angle " + str(Motor.count) + " created.")
        # creates the motor to control the wheel angle
        self.angle_motor = Motor.dxl_io.new_ax12(Motor.count)

        # sets the motor torque limit and position mode
        self.angle_motor.manual_write_lock().set_position_mode(goal_current=512)
        self.angle_motor.manual_write_lock().torque_enable()
        self.torque = True

        # increments the motor ID
        Motor.count = Motor.count + 1

        # self.bad_msg.info("Drive " + str(Motor.count) + " created.")

        # creates the motor that controls wheel velocity
        self.drive_motor = Motor.dxl_io.new_ax12(Motor.count)
        self.drive_motor.manual_write_lock().set_velocity_mode()
        self.drive_motor.manual_write_lock().torque_enable()
        Motor.count = Motor.count + 1

        # Tracks the side of the Robot the Motor is on
        self.right = side
        self.home_angle = 150

    # Toogles torque for the drive motor
    def toggle_Torque(self):
        if self.drive_motor.manual_read_lock().read_control_table("Torque_Enable") == 1:
            self.drive_motor.manual_write_lock().torque_disable()
        else:
            self.drive_motor.manual_write_lock().torque_enable()

    # Gets the current angle of the motor
    def get_angle(self):
        return self.angle_motor.manual_read_lock().get_angle()

    # Sets the angle of the motor
    def set_angle(self, angle):
        self.angle_motor.manual_write_lock().set_angle(self.home_angle - angle)

    # Sets the motor to home angle
    def center(self):
        self.set_angle(0)

    # Sets the wheel velocity
    def set_velocity(self, velocity):
        if self.right:
            self.drive_motor.manual_write_lock().set_velocity(-velocity)
        else:
            self.drive_motor.manual_write_lock().set_velocity(velocity)

    def get_velocity(self):
        return drive_motor.manual_read_lock().read_control_table("Present_Speed")
