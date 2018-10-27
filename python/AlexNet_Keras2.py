import keras,os,sys
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten,Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.utils import plot_model
from keras.callbacks import TensorBoard
import numpy as np
import random
import tflearn.datasets.oxflower17 as oxflower17

def train(x,y):
    #Create a sequential model
    model = Sequential()

    # 1st Convolutional Layer
    model.add(Conv2D(filters=96, input_shape=(224,224,3), kernel_size=11,strides=4,activation='relu',padding='valid'))
    # Pooling
    model.add(MaxPooling2D(pool_size=2, strides=2, padding='valid'))
    # Batch Normalisation before passing it to the next layer
    model.add(BatchNormalization())

    # 2nd Convolutional Layer
    model.add(Conv2D(filters=256, kernel_size=11, strides=1, activation='relu',padding='valid'))
    # Pooling
    model.add(MaxPooling2D(pool_size=2, strides=2, padding='valid'))
    # Batch Normalisation
    model.add(BatchNormalization())

    # 3rd Convolutional Layer
    model.add(Conv2D(filters=384, kernel_size=3, strides=1, activation='relu',padding='valid'))

    # 4th Convolutional Layer
    model.add(Conv2D(filters=384, kernel_size=3, strides=1, activation='relu',padding='valid'))

    # 5th Convolutional Layer
    model.add(Conv2D(filters=256, kernel_size=3, strides=1, activation='relu',padding='valid'))
    # Pooling
    model.add(MaxPooling2D(pool_size=2, strides=2, padding='valid'))

    # Passing it to a dense layer
    model.add(Flatten())

    # 1st Dense Layer
    model.add(Dense(4096,activation='relu'))
    model.add(Dropout(0.5))

    # 2nd Dense Layer
    model.add(Dense(4096,activation='relu'))
    model.add(Dropout(0.5))

    # Output Layer
    model.add(Dense(17,activation='softmax'))

    model.summary()
    # (4) Compile

    model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])

    print('Training -----------')
    tensorboard = TensorBoard(log_dir=os.getcwd()+'/llog')
    callback_lists = [tensorboard]  # 因为callback是list型,必须转化为list
    history=model.fit(x,y,batch_size=len(x), epochs=100, verbose=1,shuffle=True,callbacks=callback_lists);
    # model.fit(x, y, batch_size=64, epochs=1, verbose=1, \
    #           validation_split=0.2, shuffle=True)

    print(history.history['acc'])

    path=__file__;
    model.save(path.split('.')[0]+'_myModel.h5');

def test(x,y):
    path = __file__;
    model=keras.models.load_model(path.split('.')[0] + '_myModel.h5');
    plot_model(model, to_file='model.png',show_layer_names=True,show_shapes=True)
    loss, accuracy = model.evaluate(x, y)

    print([loss,accuracy])
    # result=[];
    # for i in range(len(x)):
    #     result.append([model.predict(x[i]),y.index(max(y))])
    # print(result)

if __name__=="__main__":
    np.random.seed(1000)

    x, y = oxflower17.load_data(one_hot=True);
    length=np.shape(x)[0];
    indexAll = list(range(0, length));
    random.shuffle(indexAll);

    alpha=0.9;
    x_train=x[indexAll[0:(int)(length*alpha)],:,:,:];
    y_train=y[indexAll[0:(int)(length*alpha)],:];

    x_test = x[indexAll[(int)(length*alpha):length],:,:,:];
    y_test = y[indexAll[(int)(length*alpha):length],:];
    # print(np.shape(x_test))
    print("train*******************************************************")
    # train(x_train,y_train);
    print("test*******************************************************")
    test(x_train,y_train);
