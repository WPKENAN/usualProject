# -*- coding: utf-8 -*-

import os
import sys
import argparse
import pandas as pd

from keras.optimizers import SGD
from keras.callbacks import ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from keras.callbacks import TensorBoard, ModelCheckpoint
from model import MSCNN
from data import generator


def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--size",
        default=224,
        help="The image size of train sample.")
    parser.add_argument(
        "--batch",
        default=16,
        help="The number of train samples per batch.")
    parser.add_argument(
        "--epochs",
        default=50,
        help="The number of train iterations.")

    args = parser.parse_args()

    train(int(args.batch), int(args.epochs),int(args.size))


def train(batch, epochs, size):
    """Train the model.

    Arguments:
        batch: Integer, The number of train samples per batch.
        epochs: Integer, The number of train iterations.
        size: Integer, image size.
    """
    if not os.path.exists('model'):
        os.makedirs('model')

    model = MSCNN((size, size, 3))
    model.summary()
    opt = SGD(lr=1e-5, momentum=0.9, decay=0.0005)
    model.compile(optimizer=opt, loss='mse')

    lr = ReduceLROnPlateau(monitor='loss', min_lr=1e-7)

    indices = list(range(1500))
    train, test = train_test_split(indices, test_size=0.25)
    logging = TensorBoard(log_dir="./model/")
    checkpoint = ModelCheckpoint("./model/" + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
                                 monitor='val_loss', save_weights_only=False, verbose=1,save_best_only=True, period=1)
    hist = model.fit_generator(
        generator(train, batch, size),
        callbacks=[checkpoint,logging,lr],
        validation_data=generator(test, batch, size),
        steps_per_epoch=len(train) // batch,
        validation_steps=len(test) // batch,
        verbose=1,
        epochs=epochs)

    model.save_weights('model\\final_weights.h5')

    df = pd.DataFrame.from_dict(hist.history)
    df.to_csv('model\\history.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv)
