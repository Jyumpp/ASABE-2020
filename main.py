import dynamixel.dynamixel_controller as d
from drive.drive import run

dxl_io = d.DynamixelIO(device_name="/dev/ttyU2D2")
motors = [dxl_io.new_mx12_1(1), dxl_io.new_mx12_1(2), dxl_io.new_mx12_1(3), dxl_io.new_mx12_1(4)]

run(dxl_io, motors)
