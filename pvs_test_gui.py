from PiVideoStreamGUI import PiVideoStream
from picamera import PiCamera
import cv2
import time

from Tkinter import *

vs = PiVideoStream()

master = Tk()
scale_iso = Scale(master,
        from_=100,
        to=1600,
        label='ISO',
        resolution=100,
        orient=HORIZONTAL)
scale_iso.pack()

shutter_speed1 = Scale(master,
        from_=1,
        to=30000,
        label='SS1',
        resolution=1,
        orient=HORIZONTAL)
shutter_speed1.pack()


shutter_speed2 = Scale(master,
        from_=1,
        to=30000,
        label='SS2',
        resolution=1,
        orient=HORIZONTAL)
shutter_speed2.pack()

scale_swap_frames = Scale(master,
        from_=1,
        to=60,
        label='swap frames',
        orient=HORIZONTAL)
scale_swap_frames.pack()

scale_ev = Scale(master,
        from_=-20,
        to=20,
        label='ev',
        orient=HORIZONTAL)
scale_ev.pack()

vs.start()

framecount = 0
swap_frames = 30

try:
    while True:
        framecount += 1
        frame = vs.read()
        cv2.imshow('Preview', frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

        master.update()

        vs.camera.iso = scale_iso.get()
        vs.camera.exposure_compensation = scale_ev.get()

        swap_frames = scale_swap_frames.get()
        if swap_frames == 1 or framecount % (swap_frames*2) > swap_frames:
            vs.camera.shutter_speed = shutter_speed1.get()
        else:
            vs.camera.shutter_speed = shutter_speed2.get()


finally:
    vs.stop()
    master.destroy()


# camera = PiCamera()
# camera.resolution = (320, 240)
# camera.framerate = 32


# vs = PiHDRVideoStream(
#         expseq=[0,600000],
#         isoseq=[100,800], 
#         framerate=60).start()
# #time.sleep(2.0)
# 
# while True:
#     frame = vs.read()
#     cv2.imshow('Preview', frame)
#     #print(vs.camera.shutter_speed)
# 
#     key = cv2.waitKey(1) & 0xff
# 
#     if key == ord('q'):
#         break
# 
# cv2.destroyAllWindows()
# vs.stop()
