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

class MODEL:
    def Vgg(width=64,height=64,depth=3,weight_decay=0.0005,classNum=0):
        model = Sequential(name='vgg16-sequential')
        input_shape=(width,height,depth)
        # 第1个卷积区块(block1)
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=input_shape, name='block1_conv1',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu', name='block1_conv2',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(MaxPool2D((2, 2), strides=(2, 2), name='block1_pool'))

        # 第2个卷积区块(block2)
        model.add(Conv2D(128, (3, 3), padding='same', activation='relu', name='block2_conv1',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(128, (3, 3), padding='same', activation='relu', name='block2_conv2',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(MaxPool2D((2, 2), strides=(2, 2), name='block2_pool'))

        # 第3个区块(block3)
        model.add(Conv2D(256, (3, 3), padding='same', activation='relu', name='block3_conv1',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(256, (3, 3), padding='same', activation='relu', name='block3_conv2',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(256, (3, 3), padding='same', activation='relu', name='block3_conv3',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(MaxPool2D((2, 2), strides=(2, 2), name='block3_pool'))

        # 第4个区块(block4)
        model.add(Conv2D(512, (3, 3), padding='same', activation='relu', name='block4_conv1',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(512, (3, 3), padding='same', activation='relu', name='block4_conv2',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(512, (3, 3), padding='same', activation='relu', name='block4_conv3',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(MaxPool2D((2, 2), strides=(2, 2), name='block4_pool'))

        # 第5个区块(block5)
        model.add(Conv2D(512, (3, 3), padding='same', activation='relu', name='block5_conv1',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(512, (3, 3), padding='same', activation='relu', name='block5_conv2',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Conv2D(512, (3, 3), padding='same', activation='relu', name='block5_conv3',kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(MaxPool2D((2, 2), strides=(2, 2), name='block5_pool'))


        # 前馈全连接区块
        model.add(Flatten(name='flatten'))
        model.add(Dense(4096, activation='relu', name='fc1'))
        model.add(Dense(4096, activation='relu', name='fc2'))
        model.add(Dense(classNum, activation='softmax', name='predictions'))

        return model

    def Lenet(width=64,height=64,depth=3,weight_decay=0.0005,classNum=0):
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
        # 第二段
        model.add(Conv2D(50, (3, 3), padding="same",kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(Conv2D(50, (3, 3), padding="same",kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))
        # 第三段
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        # softmax 分类器
        model.add(Dense(classNum))
        model.add(Activation("softmax"))

        # 返回构造的模型
        return model

def load_data(path):
    print(path)

    labels_list=os.listdir(path);
    labels_list.sort();
    print("[INFO] loading images...")
    data = []
    labels = []
    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(paths.list_images(path)))
    # print(imagePaths)
    # dda
    random.seed(42)
    random.shuffle(imagePaths)
    # loop over the input images
    for imagePath in imagePaths:
        # load the image, pre-process it, and store it in the data list
        # print(imagePath)
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)

        # extract the class label from the image path and update the
        # labels list
        # print(imagePath.split(os.path.sep)[-2])
        label = labels_list.index(imagePath.split(os.path.sep)[-2])
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # convert the labels from integers to vectors
    labels = to_categorical(labels, num_classes=CLASS_NUM)
    return data, labels


def train(aug, trainX, trainY, testX, testY):
    # initialize the model
    print("[INFO] compiling model...")
    # model = MODEL.Vgg(norm_size,norm_size,depth,0.0005,classNum=CLASS_NUM)
    model = MODEL.Lenet(norm_size, norm_size, depth, 0.0001, classNum=CLASS_NUM)
    model.summary()
    # model= keras.models.load_model('ResNet50.hdf5')
    adam = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    # sgd = SGD(decay=0.0001, momentum=0.9)
    # model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.compile(loss="categorical_crossentropy", optimizer=adam,  metrics=["accuracy"])

    # train the network
    print("[INFO] training network...")
    model_checkpoint = ModelCheckpoint('best.hdf5', monitor='val_acc', verbose=1, save_best_only=True)
    tb_cb = keras.callbacks.TensorBoard(log_dir="./log", write_images=1, histogram_freq=0)
    # 设置log的存储位置，将网络权值以图片格式保持在tensorboard中显示，设置每一个周期计算一次网络的
    # 权值，每层输出值的分布直方图
    H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),callbacks=[model_checkpoint,tb_cb],
                            validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
                            epochs=EPOCHS)

    # save the model to disk
    print("[INFO] serializing network...")
    model.save(".//lasted.model")

    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy on  classifier")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("train.png")


CLASS_NUM=0
EPOCHS = 200
INIT_LR = 1e-3
BS = 32
norm_size = 160
depth=3
if __name__ == '__main__':
    train_file_path = "./train";
    test_file_path = "./val"
    CLASS_NUM = len(os.listdir(train_file_path))

    trainX, trainY = load_data(train_file_path)
    testX, testY = load_data(test_file_path)
    # construct the image generator for data augmentation

    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                             horizontal_flip=True, fill_mode="nearest")
    train(aug, trainX, trainY, testX, testY)





