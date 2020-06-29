#!/usr/bin/python3

import time
from multiprocessing import Pipe
from dynio import *
from debugmessages import *

class DynaTrigger:

    # init
    def __init__(self, motor, home_pos, triggerPipe = None):

        # Dynamixel motor setup
        self.ax_12 = motor
        self.ax_12.torque_enable()
        self.ax_12.set_position_mode()
        self.home_pos = home_pos
        # self.ax_12.set_angle(60)
        # self.ax_12.set_velocity(1023)

        # Pipe/Shared memory setup
        self.triggerPipe = triggerPipe
        self.triggerCount = 0

        # Set up debug messages
        self.dbm = DebugMessages(self)

        # Say we've been constructed
        self.dbm.info("Constructed")

    # Process function
    def Run(self):

        while self.triggerCount < 16:

            self.ax_12.set_position_mode()
            self.ax_12.write_control_table("Torque_Limit", 1000)
            self.ax_12.set_position(self.home_pos)

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
            if self.triggerPipe is not None:
                self.triggerPipe.send(True)
            self.dbm.info("Dynamixel Triggered")

            # Wait for the motor to get back in place
            while(self.ax_12.read_control_table("Present_Load") != 0):
                pass

            if self.triggerPipe is not None:
                self.triggerPipe.send(False)
            self.ax_12.torque_enable()

        self.stop.value += 1
