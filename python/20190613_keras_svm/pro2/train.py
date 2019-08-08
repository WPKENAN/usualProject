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

CLASS_NUM=2
EPOCHS = 50
INIT_LR = 1e-4
BS = 32
norm_size = 128
depth=3
if __name__ == '__main__':
    train_file_path = "../train";
    val_file_path = "../val"
    trainList = sorted(list(paths.list_images(train_file_path)))
    valList=sorted(list(paths.list_images(val_file_path)))
    CLASS_NUM = len(os.listdir(train_file_path))

    train_datagen = ImageDataGenerator(rescale=1. / 255,rotation_range=30, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                             horizontal_flip=True, fill_mode="nearest")
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        train_file_path,
        target_size=(norm_size, norm_size),
        batch_size=BS,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        val_file_path,
        target_size=(norm_size, norm_size),
        batch_size=BS,
        class_mode='categorical')

    ###############################################################################################################################
    # initialize the model
    print("[INFO] compiling model...")
    model = MODEL.Alexnet(norm_size, norm_size, depth, 0.0005, classNum=CLASS_NUM)
    model.load_weights('keras_alexnet.hdf5', by_name=True)

    set_trainable=False
    for layer in model.layers:
        if layer.name=="new_dense3":
            set_trainable=True
        if set_trainable:
            layer.trainable=True
        else:
            layer.trainable=False
        # print(layer.name)
    model.summary()
    adam = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=adam, metrics=["accuracy"])

    # train the network
    print("[INFO] training network...")
    model_checkpoint = ModelCheckpoint('best.hdf5', monitor='val_acc', verbose=1, save_best_only=True)
    tb_cb = keras.callbacks.TensorBoard(log_dir="./log", write_images=1, histogram_freq=0)
    # 设置log的存储位置，将网络权值以图片格式保持在tensorboard中显示，设置每一个周期计算一次网络的
    H = model.fit_generator(train_generator,steps_per_epoch=len(trainList)//BS,epochs=EPOCHS,
                            validation_data=validation_generator,validation_steps=len(valList)//BS,callbacks=[model_checkpoint, tb_cb])

    # save the model to disk
    print("[INFO] serializing network...")
    model.save(".//lasted.hdf5")

    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("train.png")





