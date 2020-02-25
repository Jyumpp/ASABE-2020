#!/usr/bin/python3

from dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn
from imagecapture.imagecapture import ImageCapture as cap
from cv2 import *

captureIn = cv2.VideoCapture(1)
captureIn.set(3, 640)
captureIn.set(4, 480)

trigger = dyn(25)
capture = cap(trigger, captureIn, "/home/kevin/Documents/ASABE-2020/vision/imagecapture")