import cv2
import sys
import numpy as np

def printLum(img_file):
    img = cv2.imread(img_file)
    hsl = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,l = cv2.split(img)
    print(img_file, np.mean(l), np.std(l))

imgfiles = []

# Loop through 2-N
for i in range(len(sys.argv) - 2):
    f = sys.argv[i+2]
    imgfiles.append(f)
    print(i, f)
print('---')


for f in imgfiles:
    printLum(f)
