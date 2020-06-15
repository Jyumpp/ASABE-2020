import cv2
import math

class lineTracing:
    angle = 0
    minimum = 0
    maximum = 0
    distance = 0
    pipeAngleWrite = None
    pipeDistanceWrite = None

    def lineTracer(self):
        try:
            #capturing video, recording center point of frame with cX and cY
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
                try:
                    #preparing frame
                    frame = cv2.flip(frame, 1)
                    #greyscale conversion
                    greyVideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    #only looking at greys in this range
                    mask = cv2.inRange(greyVideo, 0, 150)
                    _,contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    #finding largest contour
                    c = max(contours, key=cv2.contourArea)
                    contours[0] = c
                    #finding an approximate triangle to represent the line
                    contx, conty, contw, conth = cv2.boundingRect(c)
                    cv2.rectangle(frame, (contx, conty), (contx + contw, conty + conth), (0, 0, 255), 2)
                    #finding top of tape
                    try:
                        list = []
                        #finding y values in the tape, within the top 15 pixels of the frame
                        for var in c:
                            if var.item(1) < 15:
                                list.append(var)
                        self.maximum = list[0].item(0)
                        #finding the rightmost value of the collected y values
                        for vat in list:
                            if vat.item(0) > self.maximum:
                                self.maximum = vat.item(0)
                        self.minimum = list[0].item(0)
                        #finding leftmost value
                        for elem in list:
                            if elem.item(0) < self.minimum:
                                self.minimum = elem.item(0)
                    except Exception as e:
                        print(e)
                        # cv2.imshow("frame", frame)
                        # cv2.waitKey(1)
                        continue

                    #top midpoint of tape
                    toppy = int(self.minimum + ((self.maximum - self.minimum) / 2))
                    #scale based on width of tape
                    scale = 23*(contw)/32
                    centerX = int(contx + (contw / 2))
                    # calculating distances and angles
                    self.angle = - math.atan((toppy - centerX) / cY)
                    self.distance = (centerX - cX)/scale
                    self.angle = math.degrees(self.angle)
                    # self.pipeAngleWrite.send(self.angle)
                    # self.pipeDistanceWrite.send(self.distance)
                    cv2.imshow("frame", frame)
                    cv2.waitKey(1)
                    #cv2.destroyAllWindows()
                    # video.release()
                    print(self.angle)
                except Exception as e:
                    pass
                    cv2.imshow("frame", frame)
                except Exception as e:
                    print(e)
                    cv2.imshow("frame", frame)
                    cv2.waitKey(1)
                    # cv2.destroyAllWindows()
                    #continue
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

    def getOrientation(self):
        return self.isVertical

    def setOrientation(self, orient):
        self.isVertical = orient

    def __init__(self):
        print("Done")

    # def __init__(self,commAngleW,commDistanceW): #self,commAngleW,commDistanceW
    #     # print()
    #     print()
    #     self.pipeAngleWrite = commAngleW
    #     self.pipeDistanceWrite = commDistanceW

test = lineTracing()

test.test()