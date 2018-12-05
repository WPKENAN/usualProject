import tensorflow as tf
input_image=tf.get_variable('image',[1,4,4,1],initializer=tf.truncated_normal_initializer(stddev=0.1));
filter_weight=tf.get_variable('weights',[4,4,1,1],initializer=tf.truncated_normal_initializer(stddev=0.1));
biases=tf.get_variable('biases',[1],initializer=tf.constant_initializer(1));
conv=tf.nn.conv2d(input_image,filter_weight,strides=[1,1,1,1],padding='SAME');
print(conv)
bias=tf.nn.bias_add(conv,biases);
actived_conv=tf.nn.relu(bias);
print(actived_conv)
pool=tf.nn.max_pool(actived_conv,ksize=[1,2,2,1],strides=[1,1,1,1],padding='SAME')
print(pool)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer());
    # print(filter_weight.eval())
    # print(sess.run(filter_weight))
    # print(sess.run(filter_weight))
    # print(pool.eval())
    # print(filter_weight.eval());
    # print("=======")
    # print(biases.eval());
    # print("conv")
    # print(conv.eval());
    # print("bias")
    # print(bias.eval());
    print("activate")
    print(actived_conv.eval());
    print("pool")
    print(pool.eval())
    # print("pool")
    # print(pool.eval());
    # print(conv.eval())
    # print(conv.eval())
    # print(input_image.eval())
    # print(input_image.eval())