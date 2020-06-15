import cv2
import math
import threading
import numpy as np

#upload to github
class lineTracking:
    angle = 0
    minimum = 0
    maximum = 0
    distance = 0

    def lineTracer(self):
        global angle
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
                greyVideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mask = cv2.inRange(greyVideo, 0, 79)
                _,contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                c = max(contours, key=cv2.contourArea)
                contours[0] = c
                #print(c)
                contx, conty, contw, conth = cv2.boundingRect(c)
                count = 0
                list = []
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
                    # cv2.imshow("frame", frame)
                    # cv2.waitKey(1)
                    continue
                toppy = int(self.minimum + ((self.maximum - self.minimum) / 2))
                cv2.rectangle(frame, (contx, conty), (contx + contw, conty + conth), (0, 0, 255), 2)
                TRy = conty
                TLx = contx
                TRx = contw + contx
                BLy = conty + conth
                BRy = conty + conth
                centerXB = int(contx + (contw / 2))
                centerXT = int(TLx + (contw / 2))
                centerY = int((BRy - TRy) / 2)
                adjacent = toppy - centerXB
                # calculating distances
                hypotenuse = math.sqrt((adjacent * adjacent) + (cY * cY))
                self.angle = math.asin(adjacent / hypotenuse)
                self.angle = math.degrees(self.angle)
                self.distance = cX - centerXB
                # cv2.imshow("frame", frame)
                # cv2.waitKey(1)
                #return angle, adjacent
                # cv2.destroyAllWindows()
                # video.release()
            except:
                # cv2.imshow("frame", frame)
                # print(sys.exc_info()[0])
                # cv2.waitKey(1)
                continue

    def test(self):
        video = cv2.VideoCapture(-1)
        while True:
            read, frame = video.read()
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            if not read:
                continue

    def getAngle(self):
        return self.angle

    def getDistance(self):
        return self.distance

    # def midPoint()

    def __init__(self):
        thread = threading.Thread(target=self.lineTracer)
        thread.setdaemon = True
        thread.start()


# liner = lineTracking()
#
# while True:
#     print(liner.getAngle())
