from keras.models import Sequential,Model
from keras.layers import Dense,Conv2D,MaxPool2D,BatchNormalization,Reshape,Flatten
from genkclf import GenClassifier
from keras.optimizers import RMSprop,Adadelta
from keras.losses import binary_crossentropy
from keras.applications.inception_v3 import InceptionV3
from keras.metrics import binary_accuracy
#符合标准定义的模型构建函数
def getmodel(input_shape):
    net=Sequential()
    net.add(Reshape(target_shape=list(input_shape)+[1],input_shape=input_shape))
    net.add(Conv2D(filters=30,kernel_size=3,activation="tanh"))
    net.add(MaxPool2D())
    net.add(Conv2D(filters=50,kernel_size=3,activation="tanh"))
    net.add(MaxPool2D())
    net.add(Conv2D(filters=20,kernel_size=3,activation="tanh"))
    net.add(MaxPool2D())
    net.add(Conv2D(filters=10, kernel_size=1, activation="tanh"))
    net.add(Flatten())
    net.add(Dense(1,activation="sigmoid"))
    net.compile(Adadelta(),loss=binary_crossentropy,metrics=[binary_accuracy])
    return net