# coding: utf-8

# import the necessary packages
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import matplotlib.pyplot as plt
import  matplotlib
matplotlib.use("Agg")
import numpy as np
import argparse
import random
import cv2
import os
import sys

class LeNet:
    @staticmethod
    def build(width, height, depth, classes):
        # initialize the model
        model = Sequential()
        inputShape = (height, width, depth)
        # if we are using "channels last", update the input shape
        if K.image_data_format() == "channels_first":   #for tensorflow
            inputShape = (depth, height, width)
        # first set of CONV => RELU => POOL layers
        model.add(Conv2D(20, (5, 5),padding="same",input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        #second set of CONV => RELU => POOL layers
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # return the constructed network architecture
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
    random.seed(42)
    random.shuffle(imagePaths)
    # loop over the input images
    # int count=0;
    for imagePath in imagePaths:
        print(imagePath)

        # load the image, pre-process it, and store it in the data list
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
    model = LeNet.build(width=norm_size, height=norm_size, depth=3, classes=CLASS_NUM)
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=opt,
                  metrics=["accuracy"])

    # train the network
    print("[INFO] training network...")
    H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
                            validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
                            epochs=EPOCHS, verbose=1)

    # save the model to disk
    print("[INFO] serializing network...")
    model.save(".//lenet5.model")

    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy on traffic-sign classifier")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig(".//")



# 我们还需要为训练设置一些参数，比如训练的epoches，batch_szie等。这些参数不是随便设的，
# 比如batch_size的数值取决于你电脑内存的大小，内存越大，batch_size就可以设为大一点。
# 又比如norm_size（图片归一化尺寸）是根据你得到的数据集，经过分析后得出的，因为我们这个数据集大多数图片的尺度都在这个范围内，
# 所以我觉得64这个尺寸应该比较合适，但是不是最合适呢？那还是要通过实验才知道的，也许64的效果更好呢？
# initialize the number of epochs to train for, initial learning rate,
# and batch size
CLASS_NUM=0
EPOCHS = 1000
INIT_LR = 1e-3
BS = 32
norm_size = 64
if __name__ == '__main__':
    train_file_path = ".\\images";
    test_file_path = ".\\images"
    CLASS_NUM = len(os.listdir(train_file_path))

    trainX, trainY = load_data(train_file_path)
    testX, testY = load_data(test_file_path)
    # construct the image generator for data augmentation

    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                             horizontal_flip=True, fill_mode="nearest")
    train(aug, trainX, trainY, testX, testY)





