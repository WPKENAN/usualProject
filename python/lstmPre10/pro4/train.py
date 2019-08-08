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
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.callbacks import ReduceLROnPlateau
from createModel import *
#直接全部预测




def train(allX,allY):
    random.seed(0)
    index = list(range(len(allY)));
    random.shuffle(index)
    # random.shuffle(index)
    # random.shuffle(index)
    allX = allX[index, :]
    allY = allY[index, :]
    val = 0.8

    x_train, y_train = allX[0:int(len(allY) * val), :], allY[0:int(len(allY) * val), :]
    x_test, y_test = allX[int(len(allY) * val):, :], allY[int(len(allY) * val):, :]

    # print(x_train.shape)
    x_train = x_train.reshape(-1, n_step, n_input)
    x_test = x_test.reshape(-1, n_step, n_input)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    mean=np.mean(x_train)
    std=np.std(x_train)

    # mean=0;
    # std=np.max(x_train)
    print("Before normalize mean:{} std:{} ".format(mean,std))
    x_train-=mean
    x_train/=std

    outfile=open("config.txt",'w')
    outfile.write("{},{}".format(mean,std));
    outfile.close()
    print("After normalize mean:{} std:{} ".format(np.mean(x_train),np.std(x_train)))
    x_test -= mean
    x_test /= std

    print(x_train.shape)
    y_train = keras.utils.to_categorical(y_train, n_classes)
    y_test = keras.utils.to_categorical(y_test, n_classes)

    # model=MODEL.Lstm(n_step, n_input,n_hidden,weight_decay,n_classes)


    # model=MODEL.Cnn(1600,weight_decay,n_classes)

    x_train=np.reshape(x_train,(x_train.shape+(1,)))
    x_test = np.reshape(x_test, (x_test.shape + (1,)))
    model=MODEL.Newnet(n_input,n_step,1,weight_decay,n_classes)

    rmsprop=keras.optimizers.RMSprop(lr=learning_rate)
    adam = Adam(lr=learning_rate)
    model.summary()
    model.compile(optimizer=adam,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model_checkpoint = ModelCheckpoint('best.hdf5', monitor='val_acc', verbose=1, save_best_only=True)
    tb_cb = keras.callbacks.TensorBoard(log_dir="./log", write_images=1, histogram_freq=0)
    reduce_lr = ReduceLROnPlateau(monitor='val_acc', patience=100, mode='auto')

    H=model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=training_iters,
              verbose=1,
              validation_data=(x_test, y_test),
              callbacks = [model_checkpoint, tb_cb,reduce_lr])

    model.save("./lasted.hdf5")
    scores = model.evaluate(x_test, y_test, verbose=0)
    print('score:', scores[0])
    print('accuracy:', scores[1])

    plt.style.use("ggplot")
    plt.figure()
    N = training_iters
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy classifier")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig("train.png")

weight_decay=0.001
learning_rate = 1e-4
training_iters = 1000
batch_size = 64
display_step = 10

n_input = 14
n_step = 4
n_hidden = 600
n_classes = 0

path="D:\github\Data\烟草红外\一阶导数数据"
target_names=sorted(os.listdir(path))
if __name__=="__main__":
    n_classes=len(os.listdir(path))
    # loaddata(path)
    allX = np.load("D:\github\Data\烟草红外\\allX.npy")[:,:1600]
    allY = np.load("D:\github\Data\烟草红外\\allY.npy")
    print(allX.shape)
    print(allY.shape)
    #
    n_input=40
    n_step=allX.shape[1]//n_input
    train(allX,allY)

# 2 804.0
# 3 536.0
# 4 402.0
# 6 268.0
# 8 201.0
# 12 134.0
# 24 67.0
# 67 24.0
# 134 12.0
# 201 8.0
# 268 6.0
# 402 4.0
# 536 3.0
# 804 2.0