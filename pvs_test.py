from PiHDRVideoStream import PiHDRVideoStream
from picamera import PiCamera
import cv2
import time

# camera = PiCamera()
# camera.resolution = (320, 240)
# camera.framerate = 32


vs = PiHDRVideoStream(
        expseq=[9,6000, 30000],
        isoseq=[100,100, 100],
        framerate=10).start()
#time.sleep(2.0)

try:
    while True:
        frame = vs.read()
        cv2.imshow('Preview', frame)
        #print(vs.camera.shutter_speed)

        key = cv2.waitKey(1) & 0xff

        if key == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    vs.stop()
