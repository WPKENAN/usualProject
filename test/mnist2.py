import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist=input_data.read_data_sets("MNIST_data",one_hot=True);
sess=tf.InteractiveSession();

x=tf.placeholder("float",shape=[None,784]);
y_=tf.placeholder("float",shape=[None,10]);

w=tf.Variable(tf.zeros([784,10]));
b=tf.Variable(tf.zeros([10]));
y=tf.nn.softmax(tf.matmul(x,w)+b);

sess.run(tf.initialize_all_variables());
cross_entropy=-tf.reduce_sum(y_*tf.log(y));
train_step=tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy);

for i in range(1000):
    batch=mnist.train.next_batch(50);
    train_step.run(feed_dict={x:batch[0],y_:batch[1]});
    correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(y_,1));
    accracy=tf.reduce_mean(tf.cast(correct_prediction,"float"));
    print("第%d代: "%(i+1));
    print(accracy.eval(feed_dict={x: mnist.test.images,y_: mnist.test.labels}));