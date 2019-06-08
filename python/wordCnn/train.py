# coding: utf-8

# import the necessary packages
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.convolutional import AveragePooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
# from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
import  matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
# import argparse
import random
import cv2
import os
# import keras
# import sys

class LeNet:
    @staticmethod
    def build(width, height, depth, classes):
        # 初始化模型
        model = Sequential()
        inputShape = (height, width, depth)
        # if we are using "channels last", update the input shape
        if K.image_data_format() == "channels_first":   #for tensorflow
            inputShape = (depth, height, width)
        # 第一段
        model.add(Conv2D(20, (5, 5),padding="same",input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))
        # 第二段
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(AveragePooling2D(pool_size=(2, 2), strides=(2, 2)))
        # 第三段
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # softmax 分类器
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # 返回构造的模型
        return model

def load_data(path):
    print(path)

    labels_list=os.listdir(path)
    labels_list.sort()
    print("[INFO] loading images...")
    data = []
    labels = []
    # 获取图像路径并打乱顺序
    imagePaths = sorted(list(paths.list_images(path)))
    random.seed(42)
    random.shuffle(imagePaths)
    # 加载图像
    for imagePath in imagePaths:
        # 加载图像，对其进行预处理，并将其存储在数据列表中
        image = cv2.imread(imagePath)
        print(imagePath)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)

        #从图像路径中提取类标签并更新标签列表
        # print(imagePath.split(os.path.sep)[-2])
        label = labels_list.index(imagePath.split(os.path.sep)[-2])
        labels.append(label)

    # 将原始像素强度缩放到范围[0，1]
    # 标准化：提高模型预测精准度，加快收敛
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # 将标签从整数转换为向量
    labels = to_categorical(labels, num_classes=CLASS_NUM)
    return data, labels


def train(aug, trainX, trainY, testX, testY):
    # 初始化模型
    print("[INFO] compiling model...")
    model = LeNet.build(width=norm_size, height=norm_size, depth=3, classes=CLASS_NUM)
    # model=keras.models.load_model(".//lenet5.model")
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=opt,
                  metrics=["accuracy"])

    # 训练网络
    print("[INFO] training network...")
    H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
                            validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
                            epochs=EPOCHS, verbose=1)

    # 绘制训练损失和准确度
    print("[INFO] serializing network...")
    model.save(".//lenet5_new.model")

    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure()
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy ")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("./lenet.png", format='png')


# 为训练设置一些参数

CLASS_NUM = 0    # 初始化类别数
EPOCHS = 100     # 迭代次数
INIT_LR = 1e-3   # adam默认学习率
BS = 32          # 总批次
norm_size = 64   # 长，宽 大小
if __name__ == '__main__':
    train_file_path = ".\\images"
    test_file_path = ".\\images"
    CLASS_NUM = len(os.listdir(train_file_path))

    trainX, trainY = load_data(train_file_path)
    testX, testY = load_data(test_file_path)

    # 构造用于数据扩充的图像生成器    图像增强
    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                             horizontal_flip=True, fill_mode="nearest")
    train(aug, trainX, trainY, testX, testY)





