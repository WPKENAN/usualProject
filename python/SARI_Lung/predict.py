from model import *
import numpy as np
import keras
from keras.callbacks import ModelCheckpoint
import cv2 as cv
import matplotlib.pylab as plt
from keras.preprocessing.image import img_to_array
import copy


avg_std=open("config").read().strip('\n').split(',')
print(avg_std)
image=cv.imread('D:\github\Data\SARI\Lung_png\\M4_GUOHONGXU0202.png')[:,:,0]
groundTruth=cv.imread('D:\github\Data\SARI\Lung_label\\M4_GUOHONGXU0202.png')[:,:,0]
org=copy.deepcopy(image)
shape=image.shape
print(image.shape)
image=cv.resize(image,(norm_size,norm_size))
image=img_to_array(image)
image=np.reshape(image,(1,)+image.shape)

image = np.array(image, dtype=np.float32)
image=(image-float(avg_std[0]))/float(avg_std[1])
model=keras.models.load_model("best.hdf5",custom_objects={'bce_dice_loss': bce_dice_loss})
result=np.round(model.predict(image))

image=image.astype(np.uint8)

thre=0.5
result[result>thre]=255
result[result<=thre]=0
result=result.astype(np.uint8)
mask=cv.resize(result[0,:,:,0],shape)

image=copy.deepcopy(org)
s=0
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        if mask[i,j]<=thre:
            image[i,j]=0;
        else:
            s=s+1
            # image[i,j]=org[i,j]
print("面积:{}".format(s))
cv.imwrite("addMask.png",image)
cv.imwrite("mask.png",mask)
print(org.shape)
print(image.shape)

cv.imshow("org_addMask",np.hstack((org,mask,groundTruth)))
cv.waitKey(0)
