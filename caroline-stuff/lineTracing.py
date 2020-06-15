# need to ensure cv is detected
import cv2
import math
import threading
import numpy as np

#handle threading
#new version of pycharm
#upload to github


def lineTracer():
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

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    greyVideo = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(greyVideo, 0, 79)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)
    contours[0] = c
    print(c)
    contx, conty, contw, conth = cv2.boundingRect(c)
    count = 0
    list = []
    print(c.size)
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
    print(maximum)
    print(minimum)
    toppy = int(minimum + ((maximum - minimum) / 2))
    cv2.rectangle(frame, (contx, conty), (contx + contw, conty + conth), (0, 0, 255), 2)
    if (contw > (width - 60)):
        edgeDetected = True
    TRy = conty
    TLx = contx
    BLy = conty + conth
    BRy = conty + conth
    centerXB = int(contx + (contw / 2))
    adjacent = toppy - centerXB
    centerXT = int(TLx + (contw / 2))
    centerY = int((BRy - TRy) / 2)
    cv2.drawContours(frame, contours, 0, (0, 255, 0), cv2.FILLED)
    cv2.circle(frame, (centerXB, cY), 7, (255, 0, 0), -1)
    # fixed
    cv2.line(frame, (centerXB, cY), (centerXB, BLy), (0, 0, 255), 2)
    # following
    cv2.line(frame, (centerXB, cY), (toppy, 0), (255, 0, 0), 2)
    adjacent = toppy - centerXB
    #distance correction
    offBy = cX - centerXB
    offByAngle = math.atan(math.abs(offBy) / cY)
    offByAngle = math.degrees((offBy/math.abs(offBy)) * offByAngle)
    # calculating distances
    hypotenuse = math.sqrt((adjacent * adjacent) + (cY * cY))
    angle = math.asin(adjacent / hypotenuse)
    angle = math.degrees(angle)
    #if looking for absolute angle
    offX = adjacent + offBy
    finalAngle = math.atan(math.abs(offX) / height)
    finalAngle = math.degrees((offX/math.abs(offX)) * finalAngle)
    cv2.imshow("frame", frame)

    return angle, adjacent
    # cv2.destroyAllWindows()
    # video.release()
