#!/usr/bin/env python
import cv2 as cv
#import picamera
import time

def loop():#camera):
    global frame, rval
    
    capture.set(15, -8.0)
    time.sleep(2)
    rval, frame1 = capture.read()
    
    capture.set(15, -3.0)
    time.sleep(2)
    rval, frame2 = capture.read()
    #rval, frame3 = capture.read()
    frame1 = frame1[0:100, 0:-1]
    frame2 = frame2[100:-1, 0:-1]

    frame[0:100,0:-1] = frame1
    frame[100:-1,0:-1] = frame2

    cv.imshow('preview', frame)
    key = cv.waitKey(20)
    if key == 27:
        return False #break
    return rval

cv.namedWindow('preview')
capture = cv.VideoCapture(-1)

if capture.isOpened():
    rval, frame = capture.read()
else:
    print('Could not open camera')
    print("Have you tried running 'sudo modprobe bcm2835-v4l2' ?")
    rval = False

if rval:
    #with picamera.PiCamera() as camera:
    while loop():#camera):
        continue

cv.destroyWindow('preview')
capture.release()
