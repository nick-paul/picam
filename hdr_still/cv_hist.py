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

if len(sys.argv) <= 3:
    print('no files in directory')
    exit(0)


imgfiles = []

# Loop through 2-N
for i in range(len(sys.argv) - 2):
    f = sys.argv[i+2]
    if 'hist' in f:
        continue
    imgfiles.append(f)
    print('   ', f)
print('---')

f, axarr = plt.subplots(len(imgfiles), figsize=(5, 8), sharex=True)

color = ('b','g','r')
for ax, imgfile in zip(axarr, imgfiles):
    # print('reading ', imgfile)
    img = cv2.imread(imgfile)

    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        ax.plot(histr,color = col)

    ax.set_xlim([0,256])
    ax.set_title(titlename(imgfile))

plt.tight_layout()

imgdir = os.path.dirname(sys.argv[2])
# output filename
outfile = sys.argv[1]
# if we are in a dir, append it
if imgdir != '':
    outfile = imgdir + '/' + outfile

plt.savefig(outfile)
#plt.show()
