#!/usr/bin/env python
import cv2 as cv
from picamera import PiCamera
import time

def loop():
    global frame, rval
    
#    capture.set(15, -8.0)
#    time.sleep(2)
    rval, frame1 = capture.read()
    
#    capture.set(15, -3.0)
#    time.sleep(2)
#    rval, frame2 = capture.read()
#    rval, frame3 = capture.read()
#    frame1 = frame1[0:100, 0:-1]
#    frame2 = frame2[100:-1, 0:-1]
#
#    frame[0:100,0:-1] = frame1
#    frame[100:-1,0:-1] = frame2

    cv.imshow('preview', frame1)
    key = cv.waitKey(20)
    if key == 27:
        return False #break
    return rval

#camera = PiCamera()

cv.namedWindow('preview')
capture = cv.VideoCapture(-1)

camera = PiCamera()

if capture.isOpened():
    rval, frame = capture.read()
else:
    print('Could not open camera')
    print("Have you tried running 'sudo modprobe bcm2835-v4l2' ?")
    rval = False

if rval:
    while loop():
        continue

cv.destroyWindow('preview')
capture.release()
