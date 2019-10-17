"""kerasmodel"""

from keras.models import Sequential,Model
from keras.layers import Dense,Conv2D,MaxPool2D,BatchNormalization,Reshape,Flatten
from genkclf import GenClassifier
from keras.optimizers import RMSprop,Adadelta
from keras.losses import binary_crossentropy
from keras.applications.inception_v3 import InceptionV3
from keras.metrics import binary_accuracy

import importlib as ipl
modelfilename="cnnmodel"

def getmodel():
    global modelfilename
    mdl=ipl.import_module(f"models.{modelfilename}")
    return mdl.getmodel(ips)
ips=[]
modelfile=""
def model(batch_size,input_shape):
    global ips
    ips=input_shape
    clf=GenClassifier(build_fn=getmodel,batch_size=batch_size)
    return clf
