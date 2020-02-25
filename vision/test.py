#!/usr/bin/python3

from dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn
from imagecapture.imagecapture import ImageCapture as cap
from cv2 import *

trigger = dyn()
capture = cap(trigger, 1, "/home/kevin/Documents/ASABE-2020/vision/imagecapture/output")