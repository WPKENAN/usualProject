import tensorflow as tf
import numpy as np

v1=tf.constant([[1.0,2.0],
                [3.0,4.0]])
v2=tf.constant([[3.0,4.0],
                [2.0,5.0]])
with tf.Session() as sess:
    print((v1*v2).eval())
    print(tf.matmul(v1,v2).eval())
    print(tf.reduce_mean(v1).eval())
    print(tf.square(v2-v1).eval())
    print(tf.reduce_sum(tf.square(v2-v1)).eval())

y_=tf.constant([1.0,0,0]);
y=tf.constant([0.5,0.4,0.1]);

cross_entropy=-tf.reduce_mean(y_*tf.log(tf.clip_by_value(y,1e-10,1.0)));
with tf.Session() as sess:
    print(cross_entropy.eval())
    print(tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y).eval())

#自定义损失函数
loss=tf.reduce_sum(tf.where(tf.greater(v1,v2),(v1-v2)*10,v2-v1));
with tf.Session() as sess:
    print(tf.greater(v1,v2).eval())
    print(tf.where(tf.greater(v1,v2),(v1-v2)*10,v2-v1).eval())
    print(loss.eval())

from numpy.random import RandomState
batch_size=8;

#输入两个节点
x=tf.placeholder(tf.float32,shape=(None,2),name='x-input');
#回归问题一般只有一个输出节点
y_=tf.placeholder(tf.float32,shape=(None,1),name='y-input');

#定义一个单层的神经网络前向传播过程，这里就是简单的加权和
w1=tf.Variable(tf.random_normal([2,1],stddev=1,seed=1));
y=tf.matmul(x,w1);

#定义预测多了和预测少了的成本
loss_less=1;
loss_more=10;
loss=tf.reduce_sum(tf.where(tf.greater(y,y_),(y-y_)*loss_more,(y_-y)*loss_less));
train_step=tf.train.AdamOptimizer(0.001).minimize(loss);

#生成一个模拟数据集
rdm=RandomState(1);
dataset_size=128;
X=rdm.rand(dataset_size,2);

#设置回归的正确值为两个输入的和加上一个随机变量
#噪音为一个均值是0的小量，噪音设置为(-0.5,0.5)的随机数
Y=[[x1+x2+rdm.rand()/10.0-0.05] for (x1,x2) in X];

#训练神经网络
with tf.Session() as sess:
    init_op=tf.global_variables_initializer();
    sess.run(init_op);
    steps=5
    for i in range(steps):

        start=(i*batch_size)%dataset_size;
        end=min(start+batch_size,dataset_size);
        sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})
        print("第 %d 次迭代:\n%s"%(i,w1.eval()))

#正则化
with tf.Session() as sess:
    print(v1.eval())
    print(sess.run(tf.contrib.layers.l1_regularizer(0.5)(v1)))
    print(sess.run(tf.contrib.layers.l2_regularizer(0.5)(v1)))


