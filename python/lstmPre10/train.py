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



def loaddata(path):
    path = "./data"
    count = 0
    for file in os.listdir(path):
        target_names.append(file)
        dataFile = os.path.join(path, file)
        data = scio.loadmat(dataFile)
        # print(data.keys())
        keys = []
        for key in data.keys():
            keys.append(key)

        # print(np.transpose(data[keys[-1]]).shape)
        x = np.transpose(data[keys[-1]])
        y = np.zeros((x.shape[0], 1)) + count

        if count == 0:
            allX = x;
            allY = y;
        else:
            allX = np.vstack((allX, x[:800, :]))
            allY = np.vstack((allY, y[:800, :]))
        count = count + 1

    return allX, allY

#直接全部预测
def predict_point_by_point():
    allX, allY = loaddata("./data")
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
    allX, allY = loaddata("./data")
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


def train():
    allX, allY = loaddata("./data")
    index = list(range(len(allY)));
    random.shuffle(index)
    allX = allX[index, :]
    allY = allY[index, :]
    val = 0.2

    x_train, y_train = allX[0:int(len(allY) * val), :], allY[0:int(len(allY) * val), :]
    x_test, y_test = allX[int(len(allY) * val):, :], allY[int(len(allY) * val):, :]

    x_train = x_train.reshape(-1, n_step, n_input)
    x_test = x_test.reshape(-1, n_step, n_input)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    # x_train /= 5
    # x_test /= 5

    y_train = keras.utils.to_categorical(y_train, n_classes)
    y_test = keras.utils.to_categorical(y_test, n_classes)
    model = Sequential()
    model.add(LSTM(n_hidden, batch_input_shape=(None, n_step, n_input), return_sequences=True))
    model.add(LSTM(n_hidden, return_sequences=False))
    model.add(Dense(n_classes))
    model.add(Activation('softmax'))

    adam = Adam(lr=learning_rate)
    model.summary()
    model.compile(optimizer=adam,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=training_iters,
              verbose=1,
              validation_data=(x_test, y_test))

    model.save("./lasted.hdf5")
    scores = model.evaluate(x_test, y_test, verbose=0)
    print('LSTM test score:', scores[0])
    print('LSTM test accuracy:', scores[1])

learning_rate = 0.001
training_iters = 20
batch_size = 64
display_step = 10

n_input = 14
n_step = 4
n_hidden = 128
n_classes = 10
target_names=[]
if __name__=="__main__":
    istrain=0;#1 是训练 0 是输出混淆阵
    if istrain:
        train();
    else:
        printMatrix()

