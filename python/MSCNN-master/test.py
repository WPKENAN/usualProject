# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sklearn.metrics as metrics

from model import MSCNN
from data import visualization
import keras


def eva_regress(y_true, y_pred):
    """Evaluation
    evaluate the predicted resul.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
    """
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)

    print('mae:%f' % mae)
    print('mse:%f' % mse)


if __name__ == '__main__':
    # name = 'data\\mall_dataset\\frames\\seq_000128.jpg'
    name="C:\\Users\Anzhi\Documents\Tencent Files\\3272346474\FileRecv\ShanghaiTech_Crowd_Counting_Dataset\part_A_final\\test_data\\images\\IMG_1.jpg"
#    name = 'data\\timg3.jpg'

    # model = MSCNN((224, 224, 3))
    # model.load_weights('model\\final_weights.h5')

    model=keras.models.load_model("best_model\\ep003-loss0.537-val_loss0.529.h5")
    img = cv2.imread(name)
    img = cv2.resize(img, (224, 224))
    img = img / 255.
    img = np.expand_dims(img, axis=0)

    dmap = model.predict(img)[0][:, :, 0]
    print(dmap)
    print('count:', int(np.sum(dmap)))
    dmap = cv2.GaussianBlur(dmap, (15, 15), 0)

    # print(max(dmap))
    print('count:', int(np.sum(dmap)))
    visualization(img[0], dmap)

