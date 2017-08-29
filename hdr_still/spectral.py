import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt


in_img = sys.argv[1]
save_plot_name = sys.argv[2]

img_color = cv2.imread(in_img)
img = cv2.imread(in_img, 0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)


rows, cols = img.shape
crow,ccol = rows/2 , cols/2
fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

plt.figure(figsize=(10,5))
plt.subplot(121),plt.imshow(img_color)
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img_back, cmap = 'jet')
plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])

plt.savefig(save_plot_name)
plt.show()
