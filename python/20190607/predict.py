from sklearn.metrics import classification_report
import numpy as np
from train import *
import keras
import os
from keras.applications.imagenet_utils import decode_predictions

if __name__=="__main__":
    all = "./images";
    val = "./val"
    CLASS_NUM = len(os.listdir(all))
    target_names=os.listdir(all)

    #x_test, Y_test = load_data(all)#全部图片
    x_test, Y_test = load_data(val)#验证集的图片

    model=keras.models.load_model("./best.hdf5")
    Y_test = np.argmax(Y_test, axis=1)  # Convert one-hot to index这里把onehot转成了整数[1,2,10,1,2,1]
    print(Y_test)
    y_pred = model.predict(x_test)  # 这里假设你的GT标注也是整数 [1,2,10,1,2,1]
    print(y_pred)
    print(y_pred.shape)
    y_pred=np.argmax(y_pred, axis=1)
    print(classification_report(Y_test, y_pred,target_names=target_names))