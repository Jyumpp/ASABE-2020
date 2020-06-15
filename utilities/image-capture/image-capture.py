#!/usr/bin/python3

from cv2 import *
import datetime

# setting up openCV
cap = cv2.VideoCapture(1) # Change this number depending on which media{} object you wish to target
cap.set(3, 640)
cap.set(4, 480)

# setting image cropping parameters
y1 = 0
y2 = 640
x1 = 180
x2 = 500

# Getting user input
greenDir = input("Please Enter the Green Output Directory: \n")
yellowDir = input("Please Enter the Yellow Output Directory: \n")
openDir = input("Please Enter the Open Output Directory: \n")

while True:

    ret, img = cap.read()
    cv2.imshow("input", img)

    key = cv2.waitKey(1)

    if key == ord('g'):

        cropped_img = img[y1:y2, x1:x2].copy()
        currentDT = datetime.datetime.now()
        fileStr = greenDir + "/green_{0:d}{1:d}{2:d}-{3:d}{4:2d}{5:d}.jpg".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second)
        cv2.imwrite(fileStr, cropped_img)

    elif key == ord('y'):
        
        cropped_img = img[y1:y2, x1:x2].copy()
        currentDT = datetime.datetime.now()
        fileStr = yellowDir + "/yellow_{0:d}{1:d}{2:d}-{3:d}{4:2d}{5:d}.jpg".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second)
        cv2.imwrite(fileStr, cropped_img)

    elif key == ord('o'):

        cropped_img = img[y1:y2, x1:x2].copy()
        currentDT = datetime.datetime.now()
        fileStr = openDir + "/open_{0:d}{1:d}{2:d}-{3:d}{4:d}{5:d}.jpg".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second)
        cv2.imwrite(fileStr, cropped_img)

    elif key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()