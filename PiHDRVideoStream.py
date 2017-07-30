# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
from Queue import Queue
import time


class PiHDRVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32, expseq=[0,15000,30000], isoseq=[100,400,800]):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=False)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        #self.frame = None
        self.stopped = False
        self.frameready = True
        self.que = Queue(maxsize=3)
        self.camera.exposure_mode = 'off'
        self.expseq = expseq
        self.isoseq = isoseq
        self.exp_idx = 0
        
        # let camera warm up
        time.sleep(2.0)
        self.camera.exposure_mode = 'off'
        

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            
            idx = self.exp_idx % 10 #len(self.expseq)
            if idx < 5:
                idx = 0
            else:
                idx = 1

            self.exp_idx += 1

            self.camera.iso = self.isoseq[idx]
            self.camera.shutter_speed = self.expseq[idx]
            print(self.camera.shutter_speed, self.camera.iso)
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.que.put(f.array)
            #self.frame = f.array
            self.frameready = True
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        self.frameready = False
        return self.que.get()

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
