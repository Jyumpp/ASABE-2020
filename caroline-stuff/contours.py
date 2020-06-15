import numpy as np
import cv2

video = cv2.VideoCapture(0)
while True:
    read, frame = video.read()
    if not read:
        continue

    #greyVideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("frame", frame)

cv2.destroyAllWindows()
video.release()