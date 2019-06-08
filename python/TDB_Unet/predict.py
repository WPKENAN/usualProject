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
image=cv.imread('D:\images\images\\1021_arterial phase_10022.png')[:,:,0]
org=copy.copy(image)
shape=image.shape
print(image.shape)
image=cv.resize(image,(256,256))
image=img_to_array(image)
image=np.reshape(image,(1,)+image.shape)

image = np.array(image, dtype=np.float32)
image=(image-float(avg_std[0]))/float(avg_std[1])
model=keras.models.load_model("best.hdf5",custom_objects={'bce_dice_loss': bce_dice_loss})
result=np.round(model.predict(image))
result=result.astype(np.uint8)
result[result>0]=255
result=cv.resize(result[0,:,:,0],shape)
cv.imwrite("result.png",result)
cv.imshow("result",np.hstack((org,result)))
cv.waitKey(0)
