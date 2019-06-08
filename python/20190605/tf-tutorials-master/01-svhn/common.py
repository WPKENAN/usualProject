#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =======================================
# File Name : common.py
# Purpose : configure the settings of 01-svhn
# Creation Date : 2019-02-19 10:30
# Last Modified :
# Created By : sunpeiqin
# =======================================

import os

class Config:
    '''where to write all the logging information during training(includes saved models)'''
    log_dir = './train_log'

    '''where to write model snapshots to'''
    log_model_dir = os.path.join(log_dir, 'models')

    exp_name = os.path.basename(log_dir)

    minibatch_size = 256
    nr_channel = 3
    image_shape = (32, 32)
    nr_class = 10
    nr_epoch = 60
    weight_decay = 1e-10

    show_interval = 100
    snapshot_interval = 2
    test_interval = 1

    use_extra_data = True

    @property
    def input_shape(self):
        return (self.minibatch_size, self.nr_channel) + self.image_shape

config = Config()
