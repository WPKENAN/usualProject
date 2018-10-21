import tensorflow as tf
logPath="tmp/log"
a = tf.constant(30.0,name='a1')
g = tf.Graph()
with g.as_default():
    c = tf.constant(30.0,name='c')
    d = tf.constant(30.0,name='d')
    e = c*d
    f = tf.divide(c,d, name='divi')

x1 = tf.Variable(1.0, name="x1");
x2 = tf.add(x1, c);
sess=tf.Session();
sess.run(tf.global_variables_initializer());
sess.run(x2)
# 指定监测结果输出目录
summary_writer = tf.summary.FileWriter(logPath, c.graph)

print(a.graph is g)
print(c.graph is g)

sess.close()