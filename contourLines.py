# need to ensure cv is detected
import cv2
import numpy as np

video = cv2.VideoCapture(0)
# not sure about dimensions here

# video
while True:
    read, frame = video.read()
    if not read:
        continue

    greyVideo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(greyVideo, 0, 0, 0)
    im2, contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    videoEdges = cv2.Canny(greyVideo, 50, 150)
    # used same dimensions with image
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imshow("frame", frame)
    cv2.imshow("edges", im2)
    # When everything done, release the capture

cv2.destroyAllWindows()
video.release()
