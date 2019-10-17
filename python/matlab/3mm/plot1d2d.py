

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
def train(x_train, x_test,y_train,y_test):
    # print(x_train.shape)

    for index in range(x_train.shape[0]):
        print(index)
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

def readNpy(path):
    data=np.load(path)
    return data

if __name__=="__main__":
    path='../data3mm.npy'
    data=readNpy(path)
    # print(data.shape)
    print(data[:,-1])
    # print(data[1,:])

    y=data[:,-1]
    x=data[:,:-1]
    x_train, x_test,y_train,y_test=train_test_split(x,y,train_size=0.9,random_state=1)
    print(x_train.shape, x_test.shape,y_train.shape,y_test.shape)
    train(x_train, x_test,y_train,y_test)