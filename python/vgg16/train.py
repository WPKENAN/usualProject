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

class Vgg:
    def build(width=64,height=64,depth=3,weight_decay=0.0005,classNum=0):
        # layer1 32*32*3
        model = Sequential()
        # 第一个 卷积层 的卷积核的数目是64 ，卷积核的大小是3*3，stride没写，默认应该是1*1
        # 对于stride=1*1,并且padding ='same',这种情况卷积后的图像shape与卷积前相同，本层后shape还是32*32
        model.add(Conv2D(64, (3, 3), padding='same',
                         input_shape=(width, height, depth), kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        # 进行一次归一化
        model.add(BatchNormalization())
        model.add(Dropout(0.3))
        # layer2 32*32*64
        model.add(Conv2D(64, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        # 下面两行代码是等价的，#keras Pool层有个奇怪的地方，stride,默认是(2*2),
        # padding默认是valid，在写代码是这些参数还是最好都加上,这一步之后,输出的shape是16*16*64
        # model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
        # layer3 16*16*64
        model.add(Conv2D(128, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        # layer4 16*16*128
        model.add(Conv2D(128, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        # layer5 8*8*128
        model.add(Conv2D(256, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        # layer6 8*8*256
        model.add(Conv2D(256, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        # layer7 8*8*256
        model.add(Conv2D(256, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        # layer8 4*4*256
        model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        # layer9 4*4*512
        model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        # layer10 4*4*512
        model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        # layer11 2*2*512
        model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        # layer12 2*2*512
        model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        # layer13 2*2*512
        model.add(Conv2D(512, (3, 3), padding='same', kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.5))
        # layer14 1*1*512
        model.add(Flatten())
        model.add(Dense(512, kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        # layer15 512
        model.add(Dense(512, kernel_regularizer=regularizers.l2(weight_decay)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        # layer16 512
        model.add(Dropout(0.5))
        model.add(Dense(classNum))
        model.add(Activation('softmax'))

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
    model = Vgg.build(norm_size,norm_size,depth,0.0005,classNum=CLASS_NUM)
    model.summary()
    # model= keras.models.load_model('ResNet50.hdf5')
    adam = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    # sgd = SGD(decay=0.0001, momentum=0.9)
    # model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.compile(loss="categorical_crossentropy", optimizer=adam,  metrics=["accuracy"])

    # train the network
    print("[INFO] training network...")
    model_checkpoint = ModelCheckpoint('Vgg.hdf5', monitor='val_acc', verbose=1, save_best_only=True)
    H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),callbacks=[model_checkpoint],
                            validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
                            epochs=EPOCHS)

    # save the model to disk
    print("[INFO] serializing network...")
    model.save(".//ResNet.model")

    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy on foot classifier")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("train.png")


CLASS_NUM=0
EPOCHS = 200
INIT_LR = 1e-3
BS = 16

norm_size = 128
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





