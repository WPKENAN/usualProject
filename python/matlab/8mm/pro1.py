import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from numpy import random
import keras
from createModel import *
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint
from keras.regularizers import l2
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.callbacks import ReduceLROnPlateau
from keras.layers import LSTM
from keras.layers import Dense, Activation
from keras.datasets import mnist
from keras.models import Sequential
from keras.optimizers import Adam

def readNpy(path):
    data=np.load(path)
    return data


def train(x_train, x_test,y_train,y_test):
    # print(x_train.shape)

    for index in range(x_train.shape[0]):
        tmp=x_train[index,:]
        # index=1200;
        plt.plot(x_train[index, :])
        plt.savefig("./1d-2d/{}-1d.jpg".format(index))
        plt.close()
        # plt.show()
        tmp=tmp.reshape(200,200);
        plt.imshow(tmp)
        plt.savefig("./1d-2d/{}-2d.jpg".format(index))
        # plt.show()
        plt.close()
        # break
    dsads


    x_train = x_train.reshape(-1, 200, 200)
    x_test = x_test.reshape(-1, 200, 200)



    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    mean = np.mean(x_train)
    std = np.std(x_train)

    # mean=0;
    # std=np.max(x_train)
    print("Before normalize mean:{} std:{} ".format(mean, std))
    x_train -= mean
    x_train /= std

    outfile = open("config.txt", 'w')
    outfile.write("{},{}".format(mean, std));
    outfile.close()
    print("After normalize mean:{} std:{} ".format(np.mean(x_train), np.std(x_train)))
    x_test -= mean
    x_test /= std

    print(x_train.shape)
    y_train = keras.utils.to_categorical(y_train, n_classes)
    y_test = keras.utils.to_categorical(y_test, n_classes)

    # model=MODEL.Lstm(n_step, n_input,n_hidden,weight_decay,n_classes)

    # model=MODEL.Cnn(1600,weight_decay,n_classes)

    x_train = np.reshape(x_train, (x_train.shape + (1,)))
    x_test = np.reshape(x_test, (x_test.shape + (1,)))
    model = MODEL.Newnet(200, 200, 1, weight_decay, n_classes)

    rmsprop = keras.optimizers.RMSprop(lr=learning_rate)
    adam = Adam(lr=learning_rate)
    model.summary()
    model.compile(optimizer=adam,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model_checkpoint = ModelCheckpoint('best.hdf5', monitor='val_acc', verbose=1, save_best_only=True)
    tb_cb = keras.callbacks.TensorBoard(log_dir="./log", write_images=1, histogram_freq=0)
    reduce_lr = ReduceLROnPlateau(monitor='val_acc', patience=100, mode='auto')

    H = model.fit(x_train, y_train,
                  batch_size=batch_size,
                  epochs=training_iters,
                  verbose=1,
                  validation_data=(x_test, y_test),
                  callbacks=[model_checkpoint, tb_cb, reduce_lr])

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

n_classes=5
weight_decay=0.001
learning_rate=1e-4
batch_size=16
training_iters=50
if __name__=="__main__":
    path='../data8mm.npy'
    data=readNpy(path)
    # print(data.shape)
    print(data[:,-1])
    # print(data[1,:])

    y=data[:,-1]
    x=data[:,:-1]
    x_train, x_test,y_train,y_test=train_test_split(x,y,train_size=0.9,random_state=1)
    print(x_train.shape, x_test.shape,y_train.shape,y_test.shape)
    train(x_train, x_test,y_train,y_test)


