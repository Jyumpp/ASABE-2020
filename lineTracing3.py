import cv2
import math
import threading
import numpy as np
import queue
import time
import sys

#upload to github
class lineTracking:
    angle = 0
    queue = queue.Queue()
    direction = ""
    minimum = 0
    maximum = 0
    edgeDetected = False
    leftTurn = False
    rightTurn = False

    def lineTracer(self):
        video = cv2.VideoCapture(-1)
        width = video.get(3)
        height = video.get(4)
        cX = int(width / 2)
        cY = int(height / 2)
        # video
        while True:
            read, frame = video.read()
            if not read:
                continue
            try:
                frame = cv2.flip(frame, 1)
                #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                greyVideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mask = cv2.inRange(greyVideo, 0, 79)
                _,contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                c = max(contours, key=cv2.contourArea)
                contours[0] = c
                #print(c)
                contx, conty, contw, conth = cv2.boundingRect(c)
                count = 0
                list = []
                #print(c.size)
                # find angle and decide how to track top right corner
                try:
                    list = []
                    for var in range(len(c)):
                        if c[var].item(1) < 1:
                            list.append(c[var])
                    self.maximum = list[0].item(0)
                    for vat in range(len(list)):
                        if list[vat].item(0) > self.maximum:
                            self.maximum = list[vat].item(0)
                    self.minimum = list[0].item(0)
                    for elem in range(len(list)):
                        if list[elem].item(0) < self.minimum:
                            self.minimum = list[elem].item(0)
                except:
                    cv2.imshow("frame", frame)
                    cv2.waitKey(1)
                    with self.queue.mutex:
                        self.queue.queue.clear()
                    self.queue.put(-720)
                #print(maximum)
                #print(minimum)
                toppy = int(self.minimum + ((self.maximum - self.minimum) / 2))
                cv2.rectangle(frame, (contx, conty), (contx + contw, conty + conth), (0, 0, 255), 2)
                TRy = conty
                TLx = contx
                TRx = contw + contx
                BLy = conty + conth
                BRy = conty + conth
                if (contw > (width - 60)):
                    self.edgeDetected = True
                    print('edge')
                elif (TRx > cX and contw > cX - 30):
                    self.rightTurn = True
                    print('right')
                elif (contx < 30 and TRx < cX + 20):
                    self.leftTurn = True
                    print('left')
                centerXB = int(contx + (contw / 2))
                centerXT = int(TLx + (contw / 2))
                centerY = int((BRy - TRy) / 2)
                #cv2.drawContours(frame, contours, 0, (0, 255, 0), cv2.FILLED)
                #cv2.circle(frame, (centerXB, cY), 7, (255, 0, 0), -1)
                # fixed
                #cv2.line(frame, (centerXB, cY), (centerXB, BLy), (0, 0, 255), 2)
                # following
                #cv2.line(frame, (centerXB, cY), (toppy, 0), (255, 0, 0), 2)
                adjacent = toppy - centerXB
                # calculating distances
                hypotenuse = math.sqrt((adjacent * adjacent) + (cY * cY))
                angle = math.asin(adjacent / hypotenuse)
                angle = math.degrees(angle)
                # with self.queue.mutex:
                #     self.queue.queue.clear()
                # if (self.edgeDetected == True):
                #     self.queue.put("edge detected")
                # if (self.rightTurn == True):
                #     self.queue.put("right turn")
                #     self.direction = "right turn"
                # elif (self.leftTurn == True):
                #     self.queue.put("left turn")
                #     self.direction = "left turn"
                # else :
                self.queue.put(angle)
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
                #return angle, adjacent
                # cv2.destroyAllWindows()
                # video.release()
            except:
                cv2.imshow("frame", frame)
                print(sys.exc_info()[0])
                cv2.waitKey(1)
                with self.queue.mutex:
                    self.queue.queue.clear()
                self.queue.put(-720)

    def test(self):
        video = cv2.VideoCapture(0)
        while True:
            read, frame = video.read()
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            if not read:
                continue

    def getAngle(self):
        return self.queue.get()

    def getDirection(self):
        return self.direction

    def __init__(self):
        thread = threading.Thread(target=self.lineTracer)
        thread.setdaemon = True
        thread.start()


# liner = lineTracking()
#
# while True:
#     print(liner.getAngle())
