#!/usr/bin/python3

import time
from multiprocessing import Pipe
from dynio import *

class DynaTrigger:

    # init
    def __init__(self, triggerPipe):

        # Dynamixel motor setup
        dxl_io = dxl.DynamixelIO('/dev/ttyUSB0', 1000000)
        self.ax_12_1 = dxl_io.new_ax12_1(7)
        self.ax_12_1.torque_enable()
        self.ax_12_1.set_position_mode()
        self.ax_12_1.set_angle(240)
        self.ax_12_1.set_velocity(1023)

        # Signal/pipe setup
        self.triggerPipe = triggerPipe
        self.triggerCount = 0

        print("Constructed")

    # Process function
    def Run(self):
        
        while self.triggerCount < 16:

            self.ax_12_1.set_position_mode()
            self.ax_12_1.write_control_table("Torque_Limit", 1000)
            self.ax_12_1.set_angle(240)

            # Wait for the motor to get into place
            while self.ax_12_1.read_control_table("Moving") == 1:
                print("1")
                pass

            # Set to velocity mode and disable torque to act like a spring
            self.ax_12_1.set_velocity_mode()
            self.ax_12_1.torque_disable()

            # Wait for trigger
            while self.ax_12_1.read_control_table("Present_Load") == 0:
                print("2")
                pass

            # increment trigger count
            self.triggerCount += 1
            # Send picture capture signal over pipe
            self.triggerPipe.send(True)
            print("trigger")

            # Wait for the motor to get back in place
            while(self.ax_12_1.read_control_table("Present_Load") != 0):
                print(self.ax_12_1.read_control_table("Present_Load"))
                print(self.ax_12_1.read_control_table("CW_Angle_Limit"))
                print(self.ax_12_1.read_control_table("CCW_Angle_Limit"))
                pass

            self.triggerPipe.send(False)
            self.ax_12_1.torque_enable()
        
