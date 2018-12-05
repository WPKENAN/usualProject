import tensorflow as tf
OUTPUT_NODE=10

IMAGE_SIZE=28
NUM_CHANNELS=1
NUM_LABELS=10

#第一层卷积的尺寸和深度
CONV1_DEEP=32
CONV1_SIZE=5;
#第二层卷积的尺寸和深度
CONV2_DEEP=64
CONV2_SIZE=5
#全连接层节点个数
FC_SIZE=512

#生成权重变量
def get_weight(shape):
    weights=tf.get_variable("weights",shape,initializer=tf.truncated_normal_initializer(stddev=0.1))
    return weights

#对卷积神经网络进行前向计算
#使用你RELU激活函数去线性化
#添加一个新的参数train，用于区分训练和测试过程
#dropout仅在训练时使用，可以进一步提升模式的可靠性并防止过拟合
def inference(input_tensor,reuse,train,regularizer):
    #定义第一层卷积层的变量并实现前向传播过程，通过使用不同的命名空间隔离不同层的变量
    #可以让每一层变量命名只考虑在当层的作用，不必担心重命名的问题
    with tf.variable_scope("layer1_conv1",reuse=reuse):
        conv1_weights=get_weight([CONV1_SIZE,CONV1_SIZE,NUM_CHANNELS,CONV1_DEEP]);
        conv1_biases=tf.get_variable("bias",[CONV1_DEEP],initializer=tf.constant_initializer(0.0));
        conv1=tf.nn.conv2d(input_tensor,conv1_weights,strides=[1,1,1,1],padding='SAME');
        relu1=tf.nn.relu(tf.nn.bias_add(conv1,conv1_biases));

    with tf.variable_scope("layer2_pool1",reuse=reuse):
        pool1=tf.nn.max_pool(relu1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME');

    with tf.variable_scope("layer3_conv2",reuse=reuse):
        conv2_weights=get_weight([CONV2_SIZE,CONV1_SIZE,CONV1_DEEP,CONV2_DEEP]);
        conv2_biases=tf.get_variable("bias",[CONV2_DEEP],initializer=tf.constant_initializer(0.0));
        conv2=tf.nn.conv2d(pool1,conv2_weights,strides=[1,1,1,1],padding="SAME");
        relu2=tf.nn.relu(tf.nn.bias_add(conv2,conv2_biases));

    with tf.variable_scope("layer4_pool2",reuse=reuse):
        pool2=tf.nn.max_pool(relu2,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME");

    #将第四层池化层的输出转化为第五层全连接层的输入格式。第四层的输出为7x7x64，然而第五层输入格式为向量
    #因为需要将矩阵拉伸为向量。因为每一层神经网络的输入输出都是一个batch的矩阵，所以这里得到的维度也包含了一个batch中矩阵的个数
    pool_shape=pool2.get_shape().as_list();
    #pool_shape[0]是一个batch里面数据的个数
    nodes=pool_shape[3]*pool_shape[2]*pool_shape[1];
    #通过tf.reshape将第四层的输出变成一个batch向量
    reshaped=tf.reshape(pool2,[pool_shape[0],nodes]);

    #dropout一般在全连接层使用
    with tf.variable_scope("layer5_fc1",reuse=reuse):
        fc1_weights=get_weight([nodes,FC_SIZE]);
        #只有全连接层的权重需要加入正则化
        if regularizer!=None:
            tf.add_to_collection("losses",regularizer(fc1_weights));
        fc1_biases=tf.get_variable("bias",[FC_SIZE],initializer=tf.constant_initializer(0.1));
        fc1=tf.nn.relu(tf.matmul(reshaped,fc1_weights)+fc1_biases);

        if train:
            fc1=tf.nn.dropout(fc1,0.5);
        with tf.variable_scope("layer6_fc2",reuse=reuse):
            fc2_weights=get_weight([FC_SIZE,NUM_LABELS]);
            if regularizer!=None:
                tf.add_to_collection('losses',regularizer(fc2_weights));
            fc2_biases=tf.get_variable('bias',[NUM_LABELS],initializer=tf.constant_initializer(0.1));
            fc2=tf.matmul(fc1,fc2_weights)+fc2_biases;
        return fc2;


