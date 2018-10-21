import tensorflow as tf
logPath="log"


a=tf.placeholder(tf.float32,(2),name="a");
b=tf.placeholder(tf.float32,(2),name="b");
c=tf.multiply(a,b,name="c");


with tf.Session() as ss:
    xsum = tf.summary.FileWriter(logPath, ss.graph)

init=tf.global_variables_initializer();
# with tf.Session() as ss:
#     ss.run(init);
#     xss=ss.run([c],feed_dict={a:[1.0,2.0],b:[3.0,4.0]});
#     print(xss)

