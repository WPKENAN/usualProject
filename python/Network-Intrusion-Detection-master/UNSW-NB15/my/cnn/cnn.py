from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Lambda
from keras.layers import Embedding
from keras.layers import Convolution1D,MaxPooling1D, Flatten
from keras.datasets import imdb
from keras import backend as K
# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
import pandas as pd
from keras.utils.np_utils import to_categorical

from sklearn.preprocessing import Normalizer
from keras.models import Sequential
from keras.layers import Convolution1D, Dense, Dropout, Flatten, MaxPooling1D
from keras.utils import np_utils
import numpy as np
import h5py
from keras import callbacks
from keras.layers import LSTM, GRU, SimpleRNN
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from keras.optimizers import SGD
from keras.models import load_model

traindata = pd.read_csv('..\\UNSW_NB15_training-set.csv')
testdata = pd.read_csv('..\\UNSW_NB15_testing-set.csv')
traindata = pd.get_dummies(data=traindata, columns=['proto', 'service', 'state'])
testdata = pd.get_dummies(data=testdata, columns=['proto', 'service', 'state'])

X = traindata.iloc[:,1:191]
Y = traindata.iloc[:,0]
C = testdata.iloc[:,0]
T = testdata.iloc[:,1:191]

scaler = Normalizer().fit(X)
trainX = scaler.transform(X)

scaler = Normalizer().fit(T)
testT = scaler.transform(T)

y_train = np.array(Y)
y_test = np.array(C)


# reshape input to be [samples, time steps, features]
X_train = np.reshape(trainX, (trainX.shape[0],trainX.shape[1],1))
X_test = np.reshape(testT, (testT.shape[0],testT.shape[1],1))




lstm_output_size = 128

cnn = Sequential()
cnn.add(Convolution1D(256, 2, border_mode="same",activation="relu",input_shape=(190, 1)))
# cnn.add(MaxPooling1D(pool_length=(2)))
# cnn.add(Flatten())
# cnn.add(Dense(512, activation="relu"))
# cnn.add(Dropout(0.5))
# cnn.add(Dense(1, activation="sigmoid"))
cnn.add(Flatten())
cnn.add(Dropout(0.4))
cnn.add(Dense(1024, activation='relu'))
cnn.add(Dense(1024, activation='relu'))
cnn.add(Dense(1024, activation='relu'))
cnn.add(Dense(1, activation="sigmoid"))

print(cnn.summary())
# define optimizer and objective, compile cnn


# cnn=load_model('cnn_model.hdf5')
# sgd = SGD(lr=0.01, nesterov=True, decay=1e-6, momentum=0.9)
cnn.compile(loss="binary_crossentropy", optimizer='adam',metrics=['accuracy'])

# train
checkpointer = callbacks.ModelCheckpoint(filepath="{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='val_acc',mode='max')
csv_logger = CSVLogger('cnntrainanalysis1.csv',separator=',', append=False)
cnn.fit(X_train, y_train, epochs=20,validation_data=(X_test, y_test),callbacks=[checkpointer,csv_logger],batch_size=256)
cnn.save("cnn_model.hdf5")

