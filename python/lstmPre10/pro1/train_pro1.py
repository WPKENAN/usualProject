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
def predict_point_by_point():
    allX, allY = loaddata(path)
    index = list(range(len(allY)));
    random.shuffle(index)
    allX = allX[index, :]
    allY = allY[index, :]

    allX=allX.reshape(-1, n_step, n_input)
    model=keras.models.load_model("./lasted.hdf5")

    predicted = model.predict(allX)
    print('predicted shape:',np.array(predicted).shape)  #(412L,1L)
    y_pred = np.argmax(predicted, axis=1)
    print(y_pred.shape)
    print(allY.shape)
    print(target_names)
    print(classification_report(allY, y_pred, target_names=target_names))

def plotCM(classes, matrix, savname):
    """classes: a list of class names"""

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix)
    fig.colorbar(cax)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            ax.text(i, j, str('%.2f' % (matrix[i, j])), va='center', ha='center',fontsize=10,color='r')
    ax.set_xticklabels([''] + classes, rotation=90,fontsize=10)
    ax.set_yticklabels([''] + classes,fontsize=10)

    # save
    # plt.savefig(savname)
    plt.show()

def printMatrix():
    allX, allY = loaddata(path)
    index = list(range(len(allY)));
    random.shuffle(index)
    allX = allX[index, :]
    allY = allY[index, :]

    allX = allX.reshape(-1, n_step, n_input)
    model = keras.models.load_model("./lasted.hdf5")

    predicted = model.predict(allX)
    print('predicted shape:', np.array(predicted).shape)  # (412L,1L)
    y_pred = np.argmax(predicted, axis=1)

    matrix = np.zeros((len(target_names),len(target_names)));
    for index in range(len(y_pred)):
        matrix[int(allY[index])][int(y_pred[index])]+=1

    #概率
    for i in range(len(target_names)):
        matrix[i,:]=matrix[i,:]/np.sum(matrix[i,:])

    plotCM(target_names, matrix, "")


def train(allX,allY):
    random.seed(0)
    index = list(range(len(allY)));
    random.shuffle(index)
    allX = allX[index, :]
    allY = allY[index, :]
    val = 0.9

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
    reduce_lr = ReduceLROnPlateau(monitor='val_acc', patience=200, mode='auto')

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

weight_decay=0.009
learning_rate = 1e-4
training_iters = 1000
batch_size = 64
display_step = 10

n_input = 14
n_step = 4
n_hidden = 600
n_classes = 0

path="../data/pro1_data"
target_names=sorted(os.listdir(path))
if __name__=="__main__":
    n_classes=len(os.listdir(path))
    # loaddata(path)
    allX = np.load("./allX.npy")[:,:1600]
    allY = np.load("./allY.npy")

    #plt.plot(allX[0,:1600])
    #plt.show()

    print(allX.shape)
    print(allY.shape)
    #
    n_input=40
    n_step=allX.shape[1]//n_input
    #train(allX,allY)

    img=allX[0,:1600]
    img=np.reshape(img,(40,40))
    plt.imshow(img, cmap='gray')
    #print(img.shape)
    #plt.show(img)
    plt.show()

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