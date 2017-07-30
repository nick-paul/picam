from PiHDRVideoStream import PiHDRVideoStream
from picamera import PiCamera
import cv2
import time

# camera = PiCamera()
# camera.resolution = (320, 240)
# camera.framerate = 32


vs = PiHDRVideoStream(expseq=[0,600000], isoseq=[100,800], framerate=20).start()
#time.sleep(2.0)

while True:
    frame = vs.read()
    cv2.imshow('Preview', frame)
    #print(vs.camera.shutter_speed)

    key = cv2.waitKey(1) & 0xff

    if key == ord('q'):
        break

cv2.destroyAllWindows()
vs.stop()
