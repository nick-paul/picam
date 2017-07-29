#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
import time 

with PiCamera() as cam:
    time.sleep(2)
    cam.exposure_mode = 'off'
#    cam.awb_mode = 'off'
    cam.iso = 100
    cam.shutter_speed = 30000 
    print(cam.shutter_speed)
    print(cam.exposure_mode)
    print(cam.iso)
    print(cam.exposure_speed)
    cam.start_preview(fullscreen=False, window=(100, 20, 640, 480))
    sleep(3)
    cam.stop_preview()


