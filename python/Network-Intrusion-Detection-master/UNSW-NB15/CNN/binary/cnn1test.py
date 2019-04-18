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
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics

# traindata = pd.read_csv('C:\\Users\Anzhi\Desktop\\Network-Intrusion-Detection-master\\UNSW-NB15\\UNSW_NB15_training-set.csv')
testdata = pd.read_csv('C:\\Users\Anzhi\Desktop\\Network-Intrusion-Detection-master\\UNSW-NB15.\\UNSW_NB15_testing-set.csv')
# traindata = pd.get_dummies(data=traindata, columns=['proto', 'service', 'state'])
testdata = pd.get_dummies(data=testdata, columns=['proto', 'service', 'state'])

# X = traindata.iloc[:,1:191]
# Y = traindata.iloc[:,0]
C = testdata.iloc[:,0]
T = testdata.iloc[:,1:191]

# scaler = Normalizer().fit(X)
# trainX = scaler.transform(X)

scaler = Normalizer().fit(T)
testT = scaler.transform(T)

# y_train = np.array(Y)
y_test = np.array(C)


# reshape input to be [samples, time steps, features]
# X_train = np.reshape(trainX, (trainX.shape[0],trainX.shape[1],1))
X_test = np.reshape(testT, (testT.shape[0],testT.shape[1],1))


lstm_output_size = 128

cnn = Sequential()
cnn.add(Convolution1D(256, 2, border_mode="same",activation="relu",input_shape=(190, 1)))
cnn.add(Flatten())
cnn.add(Dropout(0.4))
cnn.add(Dense(1024, activation='relu'))
cnn.add(Dense(1024, activation='relu'))
cnn.add(Dense(1024, activation='relu'))
cnn.add(Dense(1, activation="sigmoid"))

print(cnn.summary())

# define optimizer and objective, compile cnn
'''
cnn.compile(loss="binary_crossentropy", optimizer="adam",metrics=['accuracy'])

# train
cnn=load_model('results/cnn1results/cnn_model.hdf5')
# sgd = SGD(lr=0.01, nesterov=True, decay=1e-6, momentum=0.9)
cnn.compile(loss="binary_crossentropy", optimizer='adam',metrics=['accuracy'])

checkpointer = callbacks.ModelCheckpoint(filepath="results/cnn1results/{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='val_acc',mode='max')
csv_logger = CSVLogger('results/cnn1results/cnntrainanalysis1.csv',separator=',', append=False)
cnn.fit(X_train, y_train, epochs=20,validation_data=(X_test, y_test),callbacks=[checkpointer,csv_logger],batch_size=256)
cnn.save("results/cnn1results/cnn_model.hdf5")
'''

cnn.load_weights("results/cnn1results/cnn_model.hdf5")

#y_pred = cnn.predict_classes(X_test)

'''
np.savetxt('res/expected1.txt', y_test, fmt='%01d')
np.savetxt('res/predicted1.txt', y_pred, fmt='%01d')
cnn.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
loss, accuracy = cnn.evaluate(X_test, y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))
'''

y_pred = cnn.predict_proba(X_test)
print(y_pred)
np.savetxt("cnn.txt", y_pred)

accuracy = accuracy_score(y_test, y_pred.round(),normalize=False)
recall = recall_score(y_test, y_pred.round() , average="binary")
precision = precision_score(y_test, y_pred.round() , average="binary")
f1 = f1_score(y_test, y_pred.round(), average="binary")

print("confusion matrix")
print("----------------------------------------------")
print("accuracy")
print("%.6f" %accuracy)
print("racall")
print("%.6f" %recall)
print("precision")
print("%.6f" %precision)
print("f1score")
print("%.6f" %f1)
cm = metrics.confusion_matrix(y_test, y_pred.round())
print(cm)
print("==============================================")



