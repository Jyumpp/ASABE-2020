#!/usr/bin/python3

import time
from multiprocessing import Pipe
from dynio import *
from debugmessages.debugmessages import DebugMessages

class DynaTrigger:

    # init
    def __init__(self, triggerPipe):

        # Dynamixel motor setup
        dxl_io = dxl.DynamixelIO('/dev/ttyUSB0', 57600)
        self.ax_12 = dxl_io.new_ax12(3)
        self.ax_12.torque_enable()
        self.ax_12.set_position_mode()
        self.ax_12.set_angle(60)
        self.ax_12.set_velocity(1023)

        # Signal/pipe setup
        self.triggerPipe = triggerPipe
        self.triggerCount = 0
        self.ID = DynaTrigger.triggerCount

        # Set up debug messages
        self.dbm = DebugMessages(self)

        # Say we've been constructed
        self.dbm.info("Constructed")

    # Process function
    def Run(self):
        
        while self.triggerCount < 16:

            self.ax_12.set_position_mode()
            self.ax_12.write_control_table("Torque_Limit", 1000)
            self.ax_12.set_angle(60)

            # Wait for the motor to get into place
            while self.ax_12.read_control_table("Moving") == 1:
                pass

            # A small amount of delay to prevent multiple triggers
            time.sleep(0.5)

            # Set to velocity mode and disable torque to act like a spring
            self.ax_12.set_velocity_mode()
            self.ax_12.torque_disable()

            # Wait for trigger
            while (self.ax_12.get_current() > -50) & (self.ax_12.get_current() < 50):
                pass

            # increment trigger count
            self.triggerCount += 1
            # Send picture capture signal over pipe
            self.triggerPipe.send(True)
            self.dbm.info("Dynamixel Triggered")
            
            # Wait for the motor to get back in place
            while(self.ax_12.read_control_table("Present_Load") != 0):
                pass

            self.triggerPipe.send(False)
            self.ax_12.torque_enable()
        
