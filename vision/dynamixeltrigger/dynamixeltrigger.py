#!/usr/bin/python3

import time
import queue
from multiprocessing import Pipe
from dynio import *
from debugmessages import *
import threading


class DynaTrigger:
    count = 0
    stop = 0

    # init
    def __init__(self, motor: DynamixelMotor, home_pos, trigger_pipe):
        # Dynamixel motor setup
        self.ax_12 = motor

        self.ax_12.torque_enable()
        self.ax_12.set_position_mode()
        self.home_pos = home_pos
        # self.ax_12.set_angle(60)
        # self.ax_12.set_velocity(1023)

        # Pipe/Shared memory setup
        self.trigger_pipe = trigger_pipe
        self.trigger_count = 0
        self.count = DynaTrigger.count
        DynaTrigger.count += 1

        # Set up debug messages
        self.dbm = DebugMessages(self)

        # Say we've been constructed
        self.dbm.info("Constructed")

    # Process function
    def run(self):
        self.ax_12.set_position_mode()
        self.ax_12.write_control_table("Torque_Limit", 200)
        self.ax_12.set_position(self.home_pos)
        while self.trigger_count < 16:

            time.sleep(0.5)

            curr = self.ax_12.get_current()
            while -170 < curr < 170:
                curr = self.ax_12.get_current()

            sign = curr / abs(curr)
            self.trigger_count += 1
            if self.trigger_pipe is not None:
                self.trigger_pipe.send(True)
            self.dbm.info("Dynamixel Triggered")

            # Wait for the motor to get back in place
            while abs(self.ax_12.get_current()) > 170:
                pass

            if self.trigger_pipe is not None:
                self.trigger_pipe.send(False)

        DynaTrigger.stop += 1
