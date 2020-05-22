#!/usr/bin/python3

import time
import threading
from dynio import *

class DynaTrigger:

    # global static variable as a thread signaller
    triggered = False

    # init
    def __init__(self):

        # Dynamixel motor setup
        dxl_io = dxl.DynamixelIO('/dev/ttyUSB0', 1000000)
        self.ax_12_1 = dxl_io.new_ax12_1(7)
        self.ax_12_1.torque_enable()
        self.ax_12_1.set_angle(90)
        self.ax_12_1.set_velocity(1023)
        self.triggerCount = 0

        # Setting up Threading
        x = threading.Thread(target=self.Run)
        x.start()

    # Thread function
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

                    # Send picture capture signal
                    self.triggered = True
                    break

            # wait for the motor to get into place
            while self.ax_12_1.read_control_table('Moving') == 1:
                pass

            time.sleep(0.65)
            self.triggered = False

    def getTriggered(self):

        return self.triggered

    def getTriggerCount(self):

        return self.triggerCount
