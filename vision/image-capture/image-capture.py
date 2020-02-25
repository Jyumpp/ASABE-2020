#!/usr/bin/python3

import time
import threading
import Queue
from cv2 import *

class ImageCapture:

    def __init__(self, motorIn, cameraIn, outputIn):

        # setting the output directory for our cropped images 
        self.outputDir = outputIn
    
        # setting up openCV
        self.camera = 0
        self.camera = cameraIn
        self.cap = cv2.VideoCapture(self.camera)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        # setting image cropping parameters
        self.y1 = 0
        self.y2 = 640
        self.x1 = 180
        self.x2 = 500

        # setting up dynamixel motor
        self.motor = motorIn

        # Setting up Threading
        x = threading.Thread(target=Run)
        x.start()

    def Run(self):

        image_number = 0

        while True:

            # Get signal from motor class
            triggered = self.motor.getTriggered()

            # Capture and display the latest image
            ret, img = self.cap.read()
            cv2.imshow("input", img)

            # If the object in the queue evaluates to True, crop and save the current frame
            if triggered:
                
                # Crop and save the image in the output directory
                cropped_img = img[y1:y2, x1:x2].copy()
                fileStr = self.outputDir + "/output_{0:1d}_{1:2d}.jpg".format(self.camera, image_number)
                cv2.imwrite(fileStr, cropped_img)

                image_number += 1