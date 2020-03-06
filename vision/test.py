#!/usr/bin/python3

import time
import multiprocessing as mp
from multiprocessing import Process, Pipe
from dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn
from imagecapture.imagecapture import ImageCapture as cap
from imageclassifier.imageclassifier import ImgClassifier as classifier

if __name__ == "__main__":
    
    # Set up pipes and objects
    triggeredRead, triggeredWrite = Pipe()
    trigger = dyn(triggeredWrite)
    capture = cap(triggeredRead, -1, "/home/pi/ASABE/ASABE-2020/vision/imagecapture/output")

    # Set up processes
    mp.set_start_method('spawn')
    triggerProcess = Process(target=trigger.Run(), args=())
    captureProcess = Process(target=capture.Run(), args=())
    print("Processes Ready!")

    # Run Processes
    triggerProcess.start()
    captureProcess.start()
    print("Processes Started!")

    # Wait for the Processes to end
    triggerProcess.join()
    captureProcess.join()

    # And then classify the images we took
    time.sleep(1)
    classify = classifier("/home/pi/ASABE/ASABE-2020/vision/imagecapture/output/")
    classify.print()

