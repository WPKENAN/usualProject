import tensorflow as tf
v1=tf.Variable(tf.constant(2.0,shape=[1]),name='v1');
v2=tf.Variable(tf.constant(5.0,shape=[1]),name='v2');
result=v1+v2;
init_op=tf.global_variables_initializer();
saver=tf.train.Saver([v1]);

with tf.Session() as sess:
    sess.run(init_op);
    saver.save(sess,"./5_4_1_model.ckpt");

with tf.Session() as sess:
    sess.run(init_op);
    saver.restore(sess,"./5_4_1_model.ckpt")#v1=1 v2=2 in model
    print(sess.run(result))

with tf.Session() as sess:
    saver.restore(sess,"./5_4_1_model.ckpt")
    sess.run(init_op);
    print(sess.run(result))

v=tf.Variable(1,dtype=tf.float32,name='v');
ema=tf.train.ExponentialMovingAverage(0.99);
print(ema.variables_to_restore())