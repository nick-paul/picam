import cv2
import numpy as np
import sys
import os

# remove file extension
def rmext(f):
    return f[0:-4]

if not len(sys.argv) > 1:
    print('please supply a filename')
    exit(0)

filename = sys.argv[1]

img = cv2.imread(filename)

img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

# equalize the histogram of the Y channel
img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

# convert the YUV image back to RGB format
img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

cv2.imwrite(rmext(filename) + '_clahe.jpg', img_output)
