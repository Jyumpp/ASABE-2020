#!/usr/bin/python3

from dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn
from imagecapture.imagecapture import ImageCapture as cap
from imageclassifier.imageclassifier import ImgClassifier as classifier

trigger = dyn()
capture = cap(trigger, -1, "/home/pi/ASABE/ASABE-2020/vision/imagecapture/output")

while True:

    if trigger.getTriggerCount() == 16:
        print("required trigger count reached")
        break

#classify = classifier("/home/pi/ASABE/ASABE-2020/vision/imagecapture/output")
#classify.print()
