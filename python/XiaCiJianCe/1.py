import cv2
import numpy as np

filename = 'D:\github\Data\Paint\keli\\1.BMP'

img = cv2.imread(filename)
# print(img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
#图像转换为float32
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)#图像膨胀
# Threshold for an optimal value, it may vary depending on the image.
#print(dst)
#img[dst>0.00000001*dst.max()]=[0,0,255] #可以试试这个参数，角点被标记的多余了一些
img[dst>0.01*dst.max()]=[0,0,255]#角点位置用红色标记
#这里的打分值以大于0.01×dst中最大值为边界

img=cv2.resize(img,(512,512),interpolation=cv2.INTER_CUBIC)
cv2.imshow('dst',img)
cv2.waitKey(0)

