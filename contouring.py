# need to ensure cv is detected
import numpy as np
import cv2


video = cv2.VideoCapture(0)
while True:
    read, frame = video.read()
    if not read:
        continue

    greyVideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(greyVideo, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Frame', frame)

video.release()
cv2.destroyAllWindows()

