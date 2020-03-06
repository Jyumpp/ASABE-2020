#!/usr/bin/python3
from dynio import *

dxl_io = dxl.DynamixelIO('/dev/ttyUSB0', 1000000)
ax_12_1 = dxl_io.new_ax12_1(7)
ax_12_1.torque_enable()
ax_12_1.set_angle(90)
