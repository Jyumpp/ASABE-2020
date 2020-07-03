from Robot.Robot import *
from Robot.Motor import *
from dynio import *


dyn = dxl.DynamixelIO("/dev/ttyUSB0")
robot = Robot(dyn)
