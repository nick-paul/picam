# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
from Queue import Queue
import time

class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
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
        self.camera.image_denoise = False

        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        #self.frame = None
        self.stopped = False
        self.frameready = True
        self.que = Queue(maxsize=3)

        # Camera config

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            print(self.camera.iso, self.camera.shutter_speed, self.camera.exposure_compensation)
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
