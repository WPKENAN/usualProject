from model import *
import numpy as np
import keras
from keras.callbacks import ModelCheckpoint
import cv2 as cv
import matplotlib.pylab as plt
from keras.preprocessing.image import img_to_array
import copy
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import dicom
import os
import pydicom
import shutil
import random

def pre(model,avg_std,orgPath,labelPath,targetPath):

    image = cv.imread(orgPath)[:, :, 0]
    groundTruth = cv.imread(labelPath)[:, :, 0]
    org = copy.deepcopy(image)
    shape = image.shape
    print(image.shape)
    image = cv.resize(image, (norm_size, norm_size))
    image = img_to_array(image)
    image = np.reshape(image, (1,) + image.shape)

    image = np.array(image, dtype=np.float32)
    image = (image - float(avg_s  td[0])) / float(avg_std[1])

    result = np.round(model.predict(image))

    image = image.astype(np.uint8)

    thre = 0.5
    result[result > thre] = 255
    result[result <= thre] = 0
    result = result.astype(np.uint8)
    mask = cv.resize(result[0, :, :, 0], shape)

    image = copy.deepcopy(org)
    s = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i, j] <= thre:
                image[i, j] = 0;
            else:
                s = s + 1
                # image[i,j]=org[i,j]
    print("面积:{}".format(s))
    #cv.imwrite("addMask.png", image)
    #cv.imwrite("mask.png", mask)
    #print(org.shape)
    #print(image.shape)

    cv.imwrite(targetPath,mask)
    #cv.imshow("org_addMask", np.hstack((org, mask, groundTruth)))
    #cv.waitKey(0)

def dcm2png(dcmPath, pngPath):
    pass
def dcmTopng2(dcmPath, pngPath):
    dcm = pydicom.read_file(dcmPath)
    img = dcm.pixel_array

    img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
    img = img.astype(np.uint8)
    cv.imwrite(pngPath, img)

if __name__=="__main__":
    folder="D:\wp\BaiduNetdiskDownload\\test"
    pngFolder=folder+"/../label"
    preFolder=folder+"/../result"
    if not os.path.exists(pngFolder):
        os.mkdir(pngFolder)
    if not os.path.exists(preFolder):
        os.mkdir(preFolder)
    #print(os.listdir(pngFolder))

    for file in os.listdir(folder):
        dcmTopng2(os.path.join(folder,file),os.path.join(pngFolder,file.strip('.dcm')+".png"))

    model = keras.models.load_model("best-96.hdf5", custom_objects={'bce_dice_loss': bce_dice_loss})
    avg_std = open("config").read().strip('\n').split(',')
    print(avg_std)
    for file in os.listdir(pngFolder):
        orgPath=os.path.join(pngFolder,file)
        labelPath=os.path.join(pngFolder,file)
        targetPath=os.path.join(preFolder,file)
        pre(model,avg_std,orgPath,labelPath,targetPath)