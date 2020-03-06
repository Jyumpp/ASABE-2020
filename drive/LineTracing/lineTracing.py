import cv2
import math
import numpy as np
import sys

#upload to github
class lineTracing:
    angle = 0
    minimum = 0
    maximum = 0
    distance = 0
    isVertical = True
    pipeAngleWrite = None
    pipeDistanceWrite = None

    def lineTracer(self):
        try:
            # global angle
            video = cv2.VideoCapture(-1)
            width = video.get(3)
            height = video.get(4)
            cX = int(width / 2)
            cY = int(height / 2)
            center = (cX, cY)
            # video
            while True:
                read, frame = video.read()
                if not read:
                    continue
                try:
                    frame = cv2.flip(frame, 1)
                    frame3 = frame
                    if not self.isVertical:
                        Mat = cv2.getRotationMatrix2D(center, 270, 1.42)
                        frame = cv2.warpAffine(frame, Mat, (int(width), int(height)))
                        frame = cv2.resize(frame, (480, 640), interpolation = cv2.INTER_LINEAR)
                    frame = frame[0:][30:640]
                    greyVideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    mask = cv2.inRange(greyVideo, 0, 79)
                    _,contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    c = max(contours, key=cv2.contourArea)
                    contours[0] = c
                    # print(c)

                    #find angle and decide how to track top right corner
                    if self.isVertical:
                        Mat = cv2.getRotationMatrix2D(center, 90, 1.0)
                        frame = frame3
                        #frame = cv2.warpAffine(frame, Mat, (int(height), int(width)))
                        #frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR)

                    contx, conty, contw, conth = cv2.boundingRect(c)
                    # cv2.rectangle(frame, (contx, conty), (contx + contw, conty + conth), (0, 0, 255), 2)
                    list = []
                    try:
                        list = []
                        for var in c:
                            if var.item(1) < 1:
                                list.append(var)
                        self.maximum = list[0].item(0)
                        for vat in list:
                            if vat.item(0) > self.maximum:
                                self.maximum = vat.item(0)
                        self.minimum = list[0].item(0)
                        for elem in list:
                            if elem.item(0) < self.minimum:
                                self.minimum = elem.item(0)
                    except Exception as e:
                        cv2.imshow("frame", frame)
                        print(e)
                        cv2.waitKey(1)
                        continue

                    toppy = int(self.minimum + ((self.maximum - self.minimum) / 2))
                    TRx = contw + contx
                    BRy = conty + conth
                    scale = 23*(contw)/32
                    centerX = int(contx + (contw / 2))
                    centerY = int(conty + (conth / 2))
                    #adjacent = toppy - centerX
                    # calculating distances
                    #hypotenuse = math.sqrt((adjacent * adjacent) + (cY * cY))
                    if self.isVertical:
                        self.angle = math.atan((toppy - centerX) / cY)
                        self.distance = (centerX - cX)/scale
                    else:
                        self.angle = math.atan((toppy - centerY) / cX)
                        self.distance = ( centerY - cY) / scale
                    self.angle = math.degrees(self.angle)
                    #self.pipeAngleWrite.send(self.angle)
                    #self.pipeDistanceWrite.send(self.distance)
                    cv2.imshow("frame", frame)
                    cv2.waitKey(1)
                    #return angle, adjacent
                    #cv2.destroyAllWindows()
                    # video.release()
                    #print(self.angle)
                except Exception as e:
                    cv2.imshow("frame", frame)
                    print(e)
                    cv2.waitKey(1)
                    # cv2.destroyAllWindows()
                    #continue
                # time.sleep(.0000001)
        except Exception as e:
            print("Nope")
            print(e)
            
    def test(self):
        video = cv2.VideoCapture(-1)
        while True:
            read, frame = video.read()
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            if not read:
                continue

    # def getValues(self):
    #     return self.pipeRead.recv()

    def getOrientation(self):
        return self.isVertical

    def setOrientation(self, orient):
        self.isVertical = orient

    # def midPoint()

    def __init__(self): #self,commAngleW,commDistanceW
        print()
        #self.pipeAngleWrite = commAngleW
        #self.pipeDistanceWrite = commDistanceW
