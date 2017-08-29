import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import os

def titlename(f):
    fname = os.path.splitext(os.path.basename(f))[0]
    if fname[0:4] == 'cap_':
        return fname[4:len(fname)]
    else:
        return fname

if len(sys.argv) < 3:
    print('please provide output name and input image')
    for i, arg in zip(range(len(sys.argv)), sys.argv):
        print(' ', i, ': ', arg)
    exit(0)

imgfile = sys.argv[2]

f, (imgax, histax) = plt.subplots(1, 2, figsize=(5, 2))

color = ('b','g','r')

# print('reading ', imgfile)
img = cv2.imread(imgfile)
imgax.imshow(img)
imgax.set_title('Input Image')
imgax.axis('off')
imgax.set_yticklabels([])
imgax.set_xticklabels([])


for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    histax.plot(histr,color = col)

histax.set_xlim([0,256])
histax.set_title('Color Channel Intensity')
histax.set_yticklabels([])
histax.set_ylabel('Pixel Frequency')
histax.set_xlabel('Pixel Intensity')

plt.tight_layout()

imgdir = os.path.dirname(sys.argv[2])
# output filename
outfile = sys.argv[1]
# if we are in a dir, append it
if imgdir != '':
    outfile = imgdir + '/' + outfile

plt.savefig(outfile)
#plt.show()
