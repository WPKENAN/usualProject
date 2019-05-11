# coding=utf-8
import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile


# 图片数据文件位置，在这个文件里，每个子文件夹下代表需要区分的类别，每个子文件夹里存放了对应类别的图片
INPUT_DATA="./images"
log_dir="./log"
# Inception-v3模型瓶颈层的节点个数
BOTTLENECK_TENSOR_SIZE = 2048
# 在Inception-v3模型里代表瓶颈层结果的张量名称。在谷歌提供的Inception-v3模型里，这个张量的
# 名称就是‘pool_3/reshape:0’,在训练的模型时，可以通过tensor.name得到张量的名称
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
# 图像输入张量所对应的名称
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'

# 模型目录
MODEL_DIR = './inception_dec_2015'
# 模型文件名
MODEL_FILE = 'tensorflow_inception_graph.pb'
# 因为一个训练数据会用到很多次，因此可以将原始图像通过Inception-v3模型计算得到的特征向量保存到文件里，免去重复的计算
CACHE_DIR = ".//cache"
MODEL_2015TRAIN=".//checkpoint_dir//MyModel"



# 使用加载的训练好的Inception-v3模型处理一张图片，得到这个图片的特征向量
def run_bottleneck_on_image(sess, image_data, image_data_tensor, bottleneck_tensor):
    # 将当前图片作为输入计算瓶颈张量的值。这个瓶颈张量的值就是这张图片新的特征向量
    # print(image_data)
    bottleneck_values = sess.run(bottleneck_tensor, {image_data_tensor: image_data})
    # 经过卷积网络处理的结果是一个四维数组，需要将这个结果压缩乘一个特征向量（一维数组）
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values

# 获取一张图片经过Inception-v3模型处理之后的特征向量。
def get_bottleneck(sess, image_path,jpeg_data_tensor, bottleneck_tensor):
    # 获取原始的图片路径
    # 获取图片内容
    image_data = gfile.FastGFile(image_path, 'rb').read()
    # 计算特征向量
    bottleneck_values = run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, bottleneck_tensor)

    return bottleneck_values


def main():
    # 读取已经训练好的Inception-v3模型。
    with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    print("YES")
    # 加载读取的Inception-v3模型，并返回数据输入所对应的张量以及计算瓶颈层结果所对应的张量
    bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(
        graph_def, return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(".\\checkpoint_dir\\MyModel-10.meta");
        saver.restore(sess,tf.train.latest_checkpoint(".\\checkpoint_dir"));
        y=tf.get_collection("pred_network")[0]

        graph = tf.get_default_graph()

        input_x = graph.get_operation_by_name('BottleneckInputPlaceholder').outputs[0]
        bottleneck=get_bottleneck(sess,"C:\\Users\\Anzhi\Desktop\\1.png",jpeg_data_tensor, bottleneck_tensor);
        # print(bottleneck.shape)
        bottleneck=[float(x) for x in bottleneck]
        bottleneck=[bottleneck]
        # print(bottleneck[0])
        print("预测值是:", sess.run(y,feed_dict={input_x:bottleneck}))
        p=sess.run(y,feed_dict={input_x:bottleneck});
        tmp=0;
        for i in p:
            tmp=tmp+i;
        print(tmp)



if __name__ == '__main__':
    main()