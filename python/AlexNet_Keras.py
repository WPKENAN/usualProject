import tensorflow as tf
from tensorflow.python.keras.layers import Conv2D,MaxPool2D,Dropout,Flatten,Dense

def inference(inputs,num_classe=1000,is_training=True,dropout_keep_prob=0.5):

    '''
      Inference

      inputs: a tensor of images
      num_classes: the num of category.
      is_training: set ture when it used for training
      dropout_keep_prob: the rate of dropout during training
    '''

    x=inputs;

    #conv1
    x=Conv2D(96,[11,11],4,activation='relu',name='conv1')(x);
    #lrn1
    x=tf.nn.local_response_normalization(x,name='lrn1');
    #pool1
    x=MaxPool2D([3,3],2,name='pool1')(x)

    #conv2
    x=Conv2D(256,[5,5],activation='relu',padding='same',name='conv2')(x)
    #lrn2
    x=tf.nn.local_response_normalization(x,name='lrn2');
    #maxpool2
    x=MaxPool2D([3,3],2,name='pool2')(x)

    #conv3
    x=Conv2D(384,[3,3],activation='relu',padding='same',name='conv3')(x)

    #conv4
    x=Conv2D(384,[3,3],activation='relu',padding='same',name='conv4')(x)

    #conv5
    x=Conv2D(256,[3,3],activation='relu',padding='same',name='conv5')(x)
    #pool5
    x=MaxPool2D([3,3],2,name='pool5')(x)

    #flatten使数据扁平化
    x=Flatten(name='flatten')(x)

    if is_training:
        x=Dropout(dropout_keep_prob,name='dropout5')(x)
    #fc6
    x=Dense(4096,activation='relu',name='fc6')(x);

    if is_training:
        x=Dropout(dropout_keep_prob,name='dropout6')(x)
    x#fc7
    x=Dense(4096,activation='relu',name='fc7')(x)

    #fc8
    logits=Dense(num_classe,name='logit')(x)

    return logits;



def build_cost(logits,labels,weight_decay_rate):
    '''
      cost

      logits: predictions
      labels: true labels
      weight_decay_rate: weight_decay_rate
    '''

    with tf.variable_scope('coses'):
        '''
            tf.variable_scope可以让变量有相同的命名，包括tf.get_variable得到的变量，还有tf.Variable的变量
            tf.name_scope可以让变量有相同的命名，只是限于tf.Variable的变量
        '''
        with tf.variable_scope('xent'):
            xent=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=labels));
        with tf.variable_scope('decay'):
            costs=[]
            for var in tf.trainable_variables():
                costs.append(tf.nn.l2_loss(var));
                tf.summary.histogram(var.op.name,var);
            cost_decay=tf.multiply(weight_decay_rate,tf.add_n(costs));
        cost=tf.add(xent,cost_decay);
        tf.summary.scalar('cost',cost);
    return cost;

def build_train_op(cost,lrn_rate,global_step):
    '''
      train_op

      cost: cost
      lrn_rate: learning rate
      global_step: global step
    '''

    with tf.variable_scope('train'):
        lrn_rate = tf.constant(lrn_rate, tf.float32)
        tf.summary.scalar('learning_rate', lrn_rate)  # summary

        trainable_variables = tf.trainable_variables()
        grads = tf.gradients(cost, trainable_variables)

        optimizer = tf.train.AdamOptimizer(lrn_rate)

        apply_op = optimizer.apply_gradients(
            zip(grads, trainable_variables),
            global_step=global_step, name='train_step')

        train_op = apply_op
    return train_op

if __name__ == '__main__':
  images = tf.placeholder(tf.float32, [None, 224, 224, 3])
  labels = tf.placeholder(tf.float32, [None, 1000])
  logits = inference(inputs=images,
                     num_classe=1000)
  print('inference: good job')
  cost = build_cost(logits=logits,
                    labels=labels,
                    weight_decay_rate=0.0002)
  print('build_cost: good job')
  global_step = tf.train.get_or_create_global_step()
  train_op = build_train_op(cost=cost,
                            lrn_rate=0.001,
                            global_step=global_step)
  print('build_train_op: good job')


