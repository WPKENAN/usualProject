import tensorflow as tf

#1 加载数据
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


#2 定义超参数和placeholder
#超参数
learning_rate=0.5
epochs=10
batch_size=100

#plancholder
#输入图片维28x28 像素=784
x=tf.placeholder(tf.float32,[None,784])

#输出为0-9的one-hot编码
y=tf.placeholder(tf.float32,[None,10])

#再次强调，[None, 784]中的None表示任意值，特别对应tensor数目。

#3 定义参数w和b

#hidden layer => w b
w1=tf.Variable(tf.random_normal([784,300],stddev=0.03),name='w1')
b1=tf.Variable(tf.random_normal([300]),name='b1')

#output layer w b
w2=tf.Variable(tf.random_normal([300,10],stddev=0.03),name='w2')
b2=tf.Variable(tf.random_normal([10]),name='b2')

#4 构造隐藏层网络
#hidden layer
hidden_out=tf.add(tf.matmul(x,w1),b1);
hidden_out=tf.nn.relu(hidden_out);

#5 构造输出(预测值)
#计算输出
y_=tf.nn.softmax(tf.add(tf.matmul(hidden_out,w2),b2));

#6 bp部分定义loss
y_clipped = tf.clip_by_value(y_, 1e-10, 0.9999999)#
cross_entropy = -tf.reduce_mean(tf.reduce_sum(y * tf.log(y_clipped) + (1 - y) * tf.log(1 - y_clipped), axis=1))#n个标签计算交叉熵，对m个样本取平均


#7 BP部分—定义优化算法
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

#8 定义初始化operation和准确率node
# init operator
init_op = tf.global_variables_initializer()

# 创建准确率节点
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#9 开始训练
# 创建session
with tf.Session() as sess:
    # 变量初始化
    sess.run(init_op)
    total_batch = int(len(mnist.train.labels) / batch_size)
    for epoch in range(epochs):
        avg_cost = 0
        for i in range(total_batch):
            batch_x, batch_y = mnist.train.next_batch(batch_size=batch_size)
            _, c = sess.run([optimizer, cross_entropy], feed_dict={x: batch_x, y: batch_y})
            avg_cost += c / total_batch
        print("Epoch:", (epoch + 1), "cost = ", "{:.3f}".format(avg_cost))
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))