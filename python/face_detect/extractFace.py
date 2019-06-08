# -*- coding: utf-8 -*-

import cv2
import sys
from PIL import Image

import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2
import os

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import matplotlib.pyplot as plt
# import  matplotlib
# matplotlib.use("Agg")
# import numpy as np
# import argparse
import random
import cv2
import os
import keras
import sys


# coding=utf-8
from keras.models import Model
from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D
from keras.layers import add, Flatten
# from keras.layers.convolutional import Conv2D,MaxPooling2D,AveragePooling2D
from keras.optimizers import SGD
import numpy as np
from keras.callbacks import ModelCheckpoint

from train import *


def predictWord(model, labels_list, image):
    orig = image.copy()
    # pre-process the image for classification
    image = cv2.resize(image, (norm_size, norm_size))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    # classify the input image
    result = model.predict(image)[0]
    # print (result.shape)
    proba = np.max(result)
    print(np.where(result == proba))
    number = np.where(result == proba)[0]

    print(number)
    print(labels_list[number[0]])
    return labels_list[number[0]], proba * 100


def CatchUsbVideo(window_name, camera_idx):
    labels_list = os.listdir("./images");
    labels_list.sort();
    print(labels_list)
    # load the trained convolutional neural network
    print("[INFO] loading network...")
    model = load_model("best.hdf5")

    cv2.namedWindow(window_name)

    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)
    if not cap.isOpened():
        print("Error")
        raise IOError("Couldn't open webcam or video")

    # 告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)

    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        label_name, val = predictWord(model, labels_list, frame)

        if not ok:
            break

            # 将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # 大于0则检测到人脸
            for faceRect in faceRects:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                nameStr="This is :  {}  {:.2f}% " .format(label_name,val)
                cv2.putText(frame,text=nameStr, org=(x - 20, y - 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(0, 0, 255), thickness=2)

        # 显示图像
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

            # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    CatchUsbVideo("FaceRecongition", 0)