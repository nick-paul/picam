import cv2 as cv

cv.namedWindow('preview')
capture = cv.VideoCapture(-1)

if capture.isOpened():
    rval, frame = capture.read()
else:
    print('could not open camera')
    rval = False

while rval:
    cv.imshow('preview', frame)
    rval, frame = capture.read()
    key = cv.waitKey(20)
    if key == 27:
        break

cv.destroyWindow('preview')
capture.release()
