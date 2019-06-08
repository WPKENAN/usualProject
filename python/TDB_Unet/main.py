from model import *
from data import *
import numpy as np
import keras
from keras.callbacks import ModelCheckpoint



data_gen_args = dict(rotation_range=0.2,
                    width_shift_range=0.05,
                    height_shift_range=0.05,
                    shear_range=0.05,
                    zoom_range=0.05,
                    horizontal_flip=True,
                    fill_mode='nearest')
myGene = trainGenerator(8,'D:/images','balanceimage','balancelabel',data_gen_args,save_to_dir = None)

model = unet()
model_checkpoint = ModelCheckpoint('best.hdf5', monitor='loss',verbose=1, save_best_only=True)
tb_cb = keras.callbacks.TensorBoard(log_dir="./log", write_images=1, histogram_freq=0)
model.fit_generator(myGene,steps_per_epoch=20,epochs=100,callbacks=[model_checkpoint,tb_cb])

# testGene = testGenerator("data/membrane/test")
# results = model.predict_generator(testGene,30,verbose=1)
# saveResult("data/membrane/test",results)