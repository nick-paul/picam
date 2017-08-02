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
        if len(expseq) != len(isoseq):
            raise ValueError("len(expseq) != len(isoseq)")

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

        self.frameseq = []
        for _ in range(len(expseq)):
            self.frameseq.append(PiRGBArray(self.camera, size=resolution))

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
        self.idx = 0

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        try:
            # keep looping infinitely until the thread is stopped
            for f in self.stream:

                self.frameseq[self.idx] = f.array


                if self.idx == len(self.expseq)-1:
                    calibrate = cv2.createCalibrateDebevec()
                    response = calibrate.process(self.frameseq, self.expseq)
                    merge_debevec = cv2.createMergeDebevec()
                    hdr= merge_debevec.process(
                            self.frameseq,
                            self.expseq,
                            response)

                    self.que.put(hdr.array)

                self.rawCapture.truncate(0)

                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                if self.stopped:
                    break

                self.idx += 1
                self.idx = self.idx % len(self.expseq)

                self.camera.iso = self.isoseq[self.idx]
                self.camera.shutter_speed = self.expseq[self.idx]

                print(self.idx, self.camera.exposure_speed, self.camera.iso)
        finally:
            self.stream.close()
            self.rawCapture.close()
            self.camera.close()


    def read(self):
        # return the frame most recently read
        self.frameready = False
        return self.que.get()

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
