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
        self.ax_12_1.set_angle(90)
        self.ax_12_1.set_velocity(1023)

        # Signal/pipe setup
        self.triggerPipe = triggerPipe
        self.triggerCount = 0

    # Process function
    def Run(self):
        
        while self.triggerCount < 16:

            self.ax_12_1.set_angle(90)

            # wait for the motor to get into place
            while self.ax_12_1.read_control_table('Moving') == 1:
                pass

            time.sleep(0.65)
            while True:
                
                # If a specific torque is reached, trigger
                if self.ax_12_1.get_current() < -30:
                    
                    # incrementing trigger count
                    self.triggerCount += 1

                    # Set motor angles
                    self.ax_12_1.set_angle(30)

                    # Send picture capture signal over pipe
                    self.triggerPipe.send(True)
                    break

            # wait for the motor to get into place
            while self.ax_12_1.read_control_table('Moving') == 1:
                pass

            time.sleep(0.65)
            self.triggerPipe.send(False)
        
