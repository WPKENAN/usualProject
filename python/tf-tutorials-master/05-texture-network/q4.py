#!/usr/bin/env mdl
# -*- coding: utf-8 -*-

import os
import tensorflow as tf

from common import config
import custom_vgg16_bn as vgg16
import cv2
import numpy as np
from functools import reduce

'''use 13 convolution layers to generate gram matrix'''

GRAM_LAYERS= ['conv1_1', 'conv1_2', 'conv2_1', 'conv2_2', 'conv3_1', 'conv3_2', 'conv3_3', 'conv4_1', 'conv4_2', 'conv4_3', 'conv5_1', 'conv5_2', 'conv5_3']
image_shape = (1, 224, 224, 3)

'''you need to complete this method'''
def get_l2_gram_loss_for_layer(noise_model, image_model, layer):
    with tf.name_scope('get_l2_gram_loss_for_layer'):
        noise_map=getattr(noise_model,layer)
        image_map=getattr(image_model,layer)
        noise_gram=convert_to_gram(noise_map)
        image_gram=convert_to_gram(image_map)


        assert_equal_shapes = tf.assert_equal(noise_map.get_shape(), image_map.get_shape())
        with tf.control_dependencies([assert_equal_shapes]):
            shape = image_gram.get_shape().as_list()
            size = reduce(lambda a, b: a * b, shape)
            noise_gram_re=tf.reshape(noise_gram, [size])
            image_gram_re = tf.reshape(image_gram, [size])
            # size=1.0
            noise_gram_sorted = tf.gather(noise_gram_re, tf.nn.top_k(-noise_gram_re, k=size).indices)
            image_gram_sorted = tf.gather(image_gram_re, tf.nn.top_k(-image_gram_re, k=size).indices)
            gram_loss = get_l2_norm_loss(noise_gram_sorted - image_gram_sorted)
            return gram_loss

def get_gram_loss(noise_model, image_model):
    with tf.name_scope('get_gram_loss'):
        gram_loss = [get_l2_gram_loss_for_layer(noise_model, image_model, layer) for layer in GRAM_LAYERS ]
        gram_weights=tf.constant([1. / len(gram_loss)] * len(gram_loss), tf.float32)
    weighted_layer_losses = tf.multiply(gram_weights, tf.convert_to_tensor(gram_loss))
    return tf.reduce_sum(weighted_layer_losses)

# Compute the L2-norm divided by squared number of dimensions
def get_l2_norm_loss(diffs):
    shape = diffs.get_shape().as_list()
    size = reduce(lambda x, y: x * y, shape) ** 2
    sum_of_squared_diffs = tf.reduce_sum(tf.square(diffs))
    return sum_of_squared_diffs / size

# Given an activated filter maps of any particular layer, return its respected gram matrix
def convert_to_gram(filter_maps):
    # Get the dimensions of the filter maps to reshape them into two dimenions
    dimension = filter_maps.get_shape().as_list()
    reshaped_maps = tf.reshape(filter_maps, [dimension[1] * dimension[2], dimension[3]])
    # Compute the inner product to get the gram matrix
    if dimension[1] * dimension[2] > dimension[3]:
        return tf.matmul(reshaped_maps, reshaped_maps, transpose_a=True)
    else:
        return tf.matmul(reshaped_maps, reshaped_maps, transpose_b=True)

def output_img(session, x, save=False, out_path=None):
    shape = image_shape
    img = np.clip(session.run(x),0, 1) * 255
    img = img.astype('uint8')
    if save:
        cv2.imwrite(out_path, (np.reshape(img, shape[1:])))

def main():
    '''training a image initialized with noise'''
    pre_noise = tf.Variable(tf.random_uniform(image_shape, -3, 3 ))
    noise = tf.Variable(tf.nn.sigmoid(pre_noise))

    '''load texture image, notice that the pixel value has to be normalized to [0,1]'''
    image = cv2.imread('./images/red-peppers256.jpg')
    image = cv2.resize(image, image_shape[1:3])
    image = image.reshape(image_shape)
    image = (image/255).astype('float32')

    ''' get features of the texture image and the generated image'''
    with tf.name_scope('vgg_src'):
        image_model = vgg16.Vgg16()
        image_model.build(image)

    with tf.name_scope('vgg_noise'):
        noise_model = vgg16.Vgg16()
        noise_model.build(noise)

    ''' compute loss based on gram matrix'''
    with tf.name_scope('loss'):
        loss = get_gram_loss(noise_model, image_model)

    total_loss = loss

    global_steps = tf.Variable(0, trainable = False)
    values = [0.01, 0.005, 0.001]
    lr = tf.train.piecewise_constant(global_steps, [200, 1500], values)

    with tf.name_scope('update_image'):
        opt = tf.train.AdamOptimizer(lr)
        grads = opt.compute_gradients(total_loss, [noise])
        update_image = opt.apply_gradients(grads)

    tf.summary.scalar('loss', loss)
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(os.path.join(config.log_dir),
                                         tf.get_default_graph())

    ''' create a session '''
    tf.set_random_seed(12345) # ensure consistent results
    global_cnt = 0
    epoch_start = 0
    g_list = tf.global_variables()
    saver = tf.train.Saver(var_list=g_list)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer()) # init all variables

        ## training
        for epoch in range(epoch_start+1, config.nr_epoch+1):
            global_cnt += 1
            _, loss, summary =  sess.run([update_image, total_loss, merged],
                                        feed_dict ={ global_steps: global_cnt} )

            if global_cnt % config.show_interval == 0:
                train_writer.add_summary(summary, global_cnt)
                print(
                    "e:{}".format(epoch),'loss: {:.5f}'.format(loss),
                )

            '''save the trained image every 10 epoch'''
            if global_cnt % config.save_interval == 0 and global_cnt >0 :
                out_dir = os.path.dirname(os.path.realpath(__file__)) + './q4'

                if not os.path.isdir(out_dir):
                    os.makedirs(out_dir)
                out_dir = out_dir +'/{}.png'.format(global_cnt)
                output_img(sess, noise, save=True, out_path = out_dir)



        print('Training is done, exit.')




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os._exit(1)

# vim: ts=4 sw=4 sts=4 expandtab
