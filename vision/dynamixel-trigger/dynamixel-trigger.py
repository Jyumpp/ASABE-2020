#!/usr/bin/python3

from dynio import *
import time


# Dynamixel motor setup
dxl_io = dxl.DynamixelIO('/dev/ttyUSB0')
mx_12_1 = dxl_io.new_mx12_1(3)
mx_12_1.torque_enable()
mx_12_1.set_angle(0)

time.sleep(1)

# Loop setup
while True:

    detected = False

    mx_12_1.set_angle(90)

    time.sleep(1)

    while not detected:

        print(mx_12_1.get_current())

        if mx_12_1.get_current() > 100:

            mx_12_1.set_angle(170)
            detected = True
            # send picture capture signal
        
    time.sleep(3)



