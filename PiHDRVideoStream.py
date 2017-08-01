# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
from Queue import Queue
import time
from copy import copy

class PiHDRVideoStream:
    def __init__(self,
            resolution=(320, 240),
            framerate=62,
            expseq=[0,15000,30000],
            isoseq=[100,400,800]):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        # fix camera values
        iso=100
        time.sleep(2.0)
        self.exposure_mode = 'off'
        self.shutter_speed = 0
        gains = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = gains

        self.zeroCap= PiRGBArray(self.camera, size=resolution)
        self.rawCapture= PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                format="bgr", use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        #self.frame = None
        self.stopped = False
        self.frameready = True
        self.que = Queue(maxsize=3)
        
        self.expseq = expseq
        self.isoseq = isoseq
        self.exp_idx = 0

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            
            # idx = self.exp_idx % 4 #len(self.expseq)
            # if idx < 2:
            #     idx = 0
            # else:
            #     idx = 1

            idx = self.exp_idx % 2
            self.exp_idx += 1

            self.camera.iso = self.isoseq[idx]
            self.camera.shutter_speed = self.expseq[idx]

            print(self.camera.shutter_speed, self.camera.iso)
            
            if idx == 0:
                self.zeroCap = f.array 
            else:
                newFrame = PiRGBArray(self.camera, self.camera.resolution)

                newFrame[0:100, 0:-1] = self.zeroCap[0:100, 0:-1]
                newFrame[100:-1, 0:-1] = f[100:-1, 0:-1]

                self.que.put(newFrame.array)

            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.zeroCap.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        self.frameready = False
        return self.que.get()

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
