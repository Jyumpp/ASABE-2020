#!/usr/bin/python3

import time
from multiprocessing import Pipe
import cv2
from debugmessages.debugmessages import DebugMessages

class ImageCapture:

    def __init__(self, triggerPipe, cameraIn, outputIn):

        # setting the output directory for our cropped images 
        self.outputDir = outputIn
    
        # setting up openCV
        self.camera = cameraIn
        self.cap = cv2.VideoCapture(self.camera)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        # setting image cropping parameters
        self.y1 = 0
        self.y2 = 640
        self.x1 = 180
        self.x2 = 500

        # setting up read pipe
        self.triggerPipe = triggerPipe

        # Whitebalance calibration
        for i in range(1,25):

            ret, img = self.cap.read()

        # Setting up debugmessages
        self.dbm = DebugMessages(self)

        self.dbm.info("Camera Constructed")
        

    # Thread function
    def Run(self):

        image_number = 0

        while image_number < 16:

            # Get signal from motor class
            triggered = self.triggerPipe.recv()

            # If the object in the queue evaluates to True, crop and save the current frame
            if triggered:

                # Capture the latest image
                ret, img = self.cap.read()
                
                # Crop and save the image in the output directory
                cropped_img = img[self.y1:self.y2, self.x1:self.x2].copy()
                fileStr = self.outputDir + "/output_{0:1d}_{1:2d}.jpg".format(self.camera, image_number)
                cv2.imwrite(fileStr, cropped_img)
                self.dbm.info("Image Captured")

                # Wait until the triggered variable is back to false
                while triggered:
                    triggered = self.triggerPipe.recv()
                    pass

                image_number += 1
