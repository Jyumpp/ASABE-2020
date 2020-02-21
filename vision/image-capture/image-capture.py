#!/usr/bin/python3

import time
import threading
import Queue
from cv2 import *

class ImageCapture:

    def __init__(self, queue, camera, output):

        # setting the output directory for our cropped images 
        self.outputDir = output

        # setting up openCV
        self.cap = cv2.VideoCapture(camera)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        # setting image cropping parameters
        self.y1 = 0
        self.y2 = 640
        self.x1 = 180
        self.x2 = 500

        # Setting up queue system
        self.in_q = queue

        # Setting up Threading

    def Run(self):

        while True:
            
            image_number = 0

            # Capture and display the latest image
            ret, img = self.cap.read()
            cv2.imshow("input", img)

            # If the object in the queue evaluates to True, crop and save the current frame
            if in_q.get(block=True):
                
                # Crop and save the image in the output directory
                cropped_img = img[y1:y2, x1:x2].copy()
                fileStr = self.outputDir + "/output_{0:2d}.jpg".format(image_number)
                cv2.imwrite(fileStr, cropped_img)

                image_number += 1