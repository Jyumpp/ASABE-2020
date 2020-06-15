import cv2
import math
import threading
import numpy as np
import queue

#upload to github
class lineTracking:
    angle = 0
    queue = queue.Queue()

    def lineTracer(self):
        video = cv2.VideoCapture(0)
        width = video.get(3)
        height = video.get(4)
        cX = int(width / 2)
        cY = int(height / 2)
        # video
        while True:
            read, frame = video.read()
            if not read:
                continue
            #frame = cv2.flip(frame, 1)
            try:
                blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                greyVideo = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
                mask = cv2.inRange(greyVideo, 0, 60)
                contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                c = max(contours, key=cv2.contourArea)
                contours[0] = c
                contx, conty, contw, conth = cv2.boundingRect(c)
                list = []
                # find angle and decide how to track top right corner
                for var in range(len(c)):
                    if c[var].item(1) < 1:
                        list.append(c[var])
                maximum = list[0].item(0)
                for vat in range(len(list)):
                    if list[vat].item(0) > maximum:
                        maximum = list[vat].item(0)
                minimum = list[0].item(0)
                for elem in range(len(list)):
                    if list[elem].item(0) < minimum:
                        minimum = list[elem].item(0)
                toppy = int(minimum + ((maximum - minimum) / 2))
                cv2.rectangle(frame, (contx, conty), (contx + contw, conty + conth), (0, 0, 255), 2)
                TRx = contw + contx
                BLy = conty + conth

                if (contw > (width - 60)):
                    edgeDetected = True
                    print('edge')
                elif (TRx > cX and contw > cX - 30):
                    rightTurn = True
                    print('right')
                elif (contx < 30 and TRx < cX + 20):
                    leftTurn = True
                    print('left')
                centerXB = int(contx + (contw / 2))
                cv2.drawContours(frame, contours, 0, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (centerXB, cY), 7, (255, 0, 0), -1)
                # fixed
                cv2.line(frame, (centerXB, cY), (centerXB, BLy), (0, 0, 255), 2)
                # following
                cv2.line(frame, (centerXB, cY), (toppy, 0), (255, 0, 0), 2)
                adjacent = toppy - centerXB
                # calculating distances
                hypotenuse = math.sqrt((adjacent * adjacent) + (cY * cY))
                angle = math.asin(adjacent / hypotenuse)
                angle = math.degrees(angle)
                with self.queue.mutex:
                    self.queue.queue.clear()
                if ( edgeDetected == True):
                    self.queue.put("edge detected")
                if ( rightTurn == True):
                    self.queue.put("right turn")
                elif (leftTurn == True):
                    self.queue.put("left turn")
                else :
                    self.queue.put(angle)

            except:
                angle = 0
                continue
            cv2.imshow("frame", frame)
            cv2.waitKey(1)

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

    def __init__(self):
        thread = threading.Thread(target=self.lineTracer)
        thread.setdaemon = True
        thread.start()


liner = lineTracking()