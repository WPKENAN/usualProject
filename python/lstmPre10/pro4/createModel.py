import keras
from keras.layers import LSTM
from keras.layers import Dense, Activation
from keras.datasets import mnist
from keras.models import Sequential
from keras.optimizers import Adam
import os
import numpy as np
import scipy.io as scio
import random
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint
from keras.regularizers import l2
from keras import regularizers
from keras.layers import Dense, Dropout, Activation, Flatten,Conv1D,MaxPooling1D,GlobalAveragePooling1D,Conv2D,MaxPooling2D,GlobalMaxPooling1D
import keras.backend as K


class MODEL:
    def Lstm(n_step, n_input,n_hidden,weight_decay,n_classes):
        model = Sequential()
        model.add(LSTM(n_hidden, batch_input_shape=(None, n_step, n_input), return_sequences=True,
                       kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        model.add(LSTM(n_hidden, return_sequences=True, kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        model.add(LSTM(n_hidden, return_sequences=True, kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        model.add(LSTM(n_hidden, return_sequences=False, kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))

        model.add(Dense(4096, activation='relu', kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        model.add(Dense(4096, activation='relu', kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        model.add(Dense(1000, activation='relu', kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        model.add(Dense(n_classes, kernel_regularizer=l2(weight_decay)))
        model.add(Activation('softmax'))

        return model
    def Cnn(num_sensors,weight_decay,n_classes):
        model_m = Sequential()
        model_m.add(Conv1D(150, 3, activation='relu', padding="same",input_shape=(num_sensors,1),kernel_regularizer=l2(weight_decay)))
        model_m.add(Conv1D(64, 3, activation='relu',padding="same",kernel_regularizer=l2(weight_decay)))
        model_m.add(MaxPooling1D(2))

        # model_m.add(Conv1D(150, 3, activation='relu', padding="same", kernel_regularizer=l2(weight_decay)))
        # model_m.add(Conv1D(150, 3, activation='relu', padding="same", kernel_regularizer=l2(weight_decay)))
        # model_m.add(Conv1D(150, 3, activation='relu', padding="same", kernel_regularizer=l2(weight_decay)))
        # model_m.add(MaxPooling1D(2))
        # model_m.add(GlobalMaxPooling1D())

        # model_m.add(Conv1D(150, 3, activation='relu', padding="same", kernel_regularizer=l2(weight_decay)))
        # model_m.add(Conv1D(150, 3, activation='relu', padding="same", kernel_regularizer=l2(weight_decay)))
        # model_m.add(Conv1D(150, 3, activation='relu', padding="same", kernel_regularizer=l2(weight_decay)))
        # model_m.add(MaxPooling1D(2))

        # model_m.add(Conv1D(200, 9, activation='relu', padding="same"))
        # model_m.add(Conv1D(200, 9, activation='relu', padding="same"))
        # model_m.add(Conv1D(200, 9, activation='relu', padding="same"))
        # model_m.add(MaxPooling1D(2))

        # model_m.add(Conv1D(400, 9, activation='relu', padding="same"))
        # model_m.add(Conv1D(400, 9, activation='relu', padding="same"))
        # model_m.add(Conv1D(400, 9, activation='relu', padding="same"))
        # model_m.add(Conv1D(400, 9, activation='relu', padding="same"))
        # model_m.add(MaxPooling1D(3))

        # model_m.add(GlobalAveragePooling1D())
        model_m.add(Flatten())
        model_m.add(Dense(1024, activation='relu', kernel_regularizer=l2(weight_decay)))
        model_m.add(Dropout(0.5))
        model_m.add(Dense(1000, activation='relu', kernel_regularizer=l2(weight_decay)))
        model_m.add(Dropout(0.5))
        model_m.add(Dense(n_classes, activation='softmax'))
        print(model_m.summary())
        return model_m

    def Newnet(width=64, height=64, depth=3, weight_decay=0.0005, classNum=0):
        # 初始化模型
        model = Sequential()
        inputShape = (height, width, depth)
        # if we are using "channels last", update the input shape
        if K.image_data_format() == "channels_first":  # for tensorflow
            inputShape = (depth, height, width)
        # 第一段
        model.add(Conv2D(256, (3, 3), padding="same",activation='relu', input_shape=inputShape,kernel_regularizer=regularizers.l2(weight_decay),kernel_initializer='he_normal'))
        model.add(Conv2D(256, (3, 3), padding="same", activation='relu', kernel_regularizer=regularizers.l2(weight_decay),kernel_initializer='he_normal'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(256, (3, 3), padding="same", activation='relu', kernel_regularizer=regularizers.l2(weight_decay),kernel_initializer='he_normal'))
        model.add(Conv2D(256, (3, 3), padding="same", activation='relu', kernel_regularizer=regularizers.l2(weight_decay),kernel_initializer='he_normal'))
        # model.add(Conv2D(256, (3, 3), padding="same", activation='relu', kernel_regularizer=regularizers.l2(weight_decay),kernel_initializer='he_normal'))
        #model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))

        # 第二段
        # model.add(Conv2D(130, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(130, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(30, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(30, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))

        # 第三段
        # model.add(Conv2D(100, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(100, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(100, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(100, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(100, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(100, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(Conv2D(100, (3, 3), padding="same", kernel_regularizer=regularizers.l2(weight_decay)))
        # model.add(Activation("relu"))
        # model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # 第4段
        model.add(Flatten())
        model.add(Dense(1024, activation='relu', kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        # model.add(Dense(1000, activation='relu', kernel_regularizer=l2(weight_decay),kernel_initializer='he_normal'))
        # model.add(Dropout(0.5))
        model.add(Dense(1000, activation='relu', kernel_regularizer=l2(weight_decay)))
        model.add(Dropout(0.5))
        # softmax 分类器
        model.add(Dense(classNum))
        model.add(Activation("softmax"))

        # 返回构造的模型
        return model