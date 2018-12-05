import tensorflow as tf
v1=tf.Variable(tf.constant(2.0,shape=[1]),name='v1');
v2=tf.Variable(tf.constant(5.0,shape=[1]),name='v2',trainable=False);
result=v1+v2;
saver=tf.train.Saver();
saver.export_meta_graph("./5_4_2_model.ckpt.meda.json",as_text=True)