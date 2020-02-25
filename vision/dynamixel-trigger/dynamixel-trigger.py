#!/usr/bin/python3

import time
import threading
import Queue
from dynio import *

class DynaTrigger(self):

    # global static variable as a thread signaller
    triggered = False

    # init
    def __init__(self, torqueIn):

        # Dynamixel motor setup
        self.dxl_io = dxl.DynamixelIO('/dev/ttyUSB0', 1000000)
        self.ax_12_1 = dxl_io.new_ax12_1(7)
        self.ax_12_1.torque_enable()
        self.ax_12_1.set_angle(0)
        self.ax_12_1.set_velocity(1023)
        self.torque = torqueIn

        # Setting up Threading
        

    # Thread function
    def Run(self):
        
        while True:

            self.ax_12_1.set_angle(90)

            time.sleep(0.75)

            while True:
                
                # If a specific torque is reached, trigger
                if self.ax_12_1.get_current() > self.torque:
                    
                    # Set motor angles
                    self.ax_12_1.set_angle(170)

                    # Send picture capture signal
                    self.triggered = True
                    time.sleep 
                    break
        
            self.triggered = False

            # wait for the motor to get into place
            time.sleep(0.25)

    def getTriggered(self):

        return self.triggered