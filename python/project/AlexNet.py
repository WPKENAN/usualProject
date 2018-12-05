from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
mnist=input_data.read_data_sets("/tmp/data/",one_hot=True);

#定义超参数
learning_date=0.001;
train_iters=20000;
batch_size=128;
display_step=10;

#定义网格参数
n_input=784 #输入维度28x28
n_classes=10; #标记的维度0-9
dropout=0.75; #drop的概率

#占位符
x=tf.placeholder(tf.float32,[None,n_input]);
y=tf.placeholder(tf.float32,[None,n_classes]);
keep_prob=tf.placeholder(tf.float32); #dropout

#卷积操作
def conv2d(name,x,W,b,strides=1):
    x=tf.nn.conv2d(x,W,strides=[1,strides,strides,1],padding='SAME');
    x=tf.nn.bias_add(x,b);
    return tf.nn.relu(x,name=name); #用relu激活函数

#池化
def maxpool2d(name,x,k=2):
    return tf.nn.max_pool(x,ksize=[1,k,k,1],strides=[1,k,k,1],padding='SAME',name=name);

#规范化操作
def norm(name,l_input,lsize=4):
    return tf.nn.lrn(l_input,lsize,bias=1.0,alpha=0.001/9.0,beta=0.75,name=name);

weights={
    'wc1': tf.Variable(tf.random_normal([11, 11, 1, 96])),
    'wc2': tf.Variable(tf.random_normal([5, 5, 96, 256])),
    'wc3': tf.Variable(tf.random_normal([3, 3, 256, 384])),
    'wc4': tf.Variable(tf.random_normal([3, 3, 384, 384])),
    'wc5': tf.Variable(tf.random_normal([3, 3, 384, 256])),
    'wd1': tf.Variable(tf.random_normal([4*4*256, 4096])),
    'wd2': tf.Variable(tf.random_normal([4096, 4096])),
    'out': tf.Variable(tf.random_normal([4096, 10]))
}

biases = {
    'bc1': tf.Variable(tf.random_normal([96])),
    'bc2': tf.Variable(tf.random_normal([256])),
    'bc3': tf.Variable(tf.random_normal([384])),
    'bc4': tf.Variable(tf.random_normal([384])),
    'bc5': tf.Variable(tf.random_normal([256])),
    'bd1': tf.Variable(tf.random_normal([4096])),
    'bd2': tf.Variable(tf.random_normal([4096])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# 定义AlexNet网络模型
def alex_net(x,weights,biases,dropout):
    #向量转化为矩阵
    x=tf.reshape(x,shape=[-1,28,28,1]);

    #第一个卷积层
    conv1=conv2d('conv1',x,weights['wc1'],biases['bc1'])
