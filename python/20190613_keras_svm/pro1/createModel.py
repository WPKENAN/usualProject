# coding: utf-8

# import the necessary packages

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
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras import regularizers


# coding=utf-8
from keras.models import Model
from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPooling2D, AveragePooling2D, ZeroPadding2D
from keras.layers import add, Flatten
# from keras.layers.convolutional import Conv2D,MaxPooling2D,AveragePooling2D
from keras.optimizers import SGD
import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.callbacks import TensorBoard
from keras import backend as K
from keras.layers import Conv2D,MaxPool2D
from createModel import *


class MODEL:
    def Alexnet(width=64,height=64,depth=3,weight_decay=0.0005,classNum=0):
        # AlexNet
        inputShape = (height, width, depth)
        model = Sequential()
        # 第一段
        model.add(Conv2D(filters=96, kernel_size=(11, 11),strides=(4, 4),
                         padding='valid',input_shape=inputShape,activation='relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(3, 3),strides=(2, 2),padding='valid'))
        # 第二段
        model.add(Conv2D(filters=256, kernel_size=(5, 5),strides=(1, 1),
                         padding='same',activation='relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(3, 3),strides=(2, 2),padding='valid'))
        # 第三段
        model.add(Conv2D(filters=384, kernel_size=(3, 3),strides=(1, 1),
                         padding='same',activation='relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(filters=384, kernel_size=(3, 3),strides=(1, 1),
                         padding='same',activation='relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(filters=256, kernel_size=(3, 3),strides=(1, 1),
                         padding='same',activation='relu',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(MaxPooling2D(pool_size=(3, 3),strides=(2, 2), padding='valid'))
        # 第四段
        model.add(Flatten())
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1000, activation='relu'))
        model.add(Dropout(0.5))
        # Output Layer
        model.add(Dense(2))
        model.add(Activation('softmax'))

        return model



    def Lenet(width=64,height=64,depth=3,weight_decay=0.0005,classNum=0):
        # 初始化模型
        model = Sequential()
        inputShape = (height, width, depth)
        # if we are using "channels last", update the input shape
        if K.image_data_format() == "channels_first":  # for tensorflow
            inputShape = (depth, height, width)
        # 第一段
        model.add(Conv2D(20, (5, 5), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        # model.add(Conv2D(20, (5, 5), padding="same"))
        # model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))
        # 第二段
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        # model.add(Conv2D(50, (3, 3), padding="same"))
        # model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))

        # model.add(Conv2D(50, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(50, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(50, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # 第4段
        model.add(Flatten())
        model.add(Dense(1000))
        model.add(Activation("relu"))
        # model.add(Dropout(0.5))

        # softmax 分类器
        model.add(Dense(classNum))
        model.add(Activation("softmax"))

        # 返回构造的模型
        return model

    def Newnet(width=64,height=64,depth=3,weight_decay=0.0005,classNum=0):
        # 初始化模型
        model = Sequential()
        inputShape = (height, width, depth)
        # if we are using "channels last", update the input shape
        if K.image_data_format() == "channels_first":   #for tensorflow
            inputShape = (depth, height, width)
        # 第一段
        model.add(Conv2D(20, (3, 3),padding="same",input_shape=inputShape,kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(Conv2D(20, (3, 3), padding="same",kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))
        #第二段
        model.add(Conv2D(30, (3, 3), padding="same",kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(Conv2D(30, (3, 3), padding="same",kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))

        #第三段
        model.add(Conv2D(50, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(Conv2D(50, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(Conv2D(50, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # 第4段
        model.add(Flatten())
        model.add(Dense(1000))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        # softmax 分类器
        model.add(Dense(classNum))
        model.add(Activation("softmax"))

        # 返回构造的模型
        return model