#encoding=utf-8
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

# coding=utf-8
import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

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




# 将数据文件夹的图片按照训练，验证和测试数据分开
def create_image_lists():
    # 得到的所有图片都存在result这个字典里，这个字典的key为类别的名称，value也是一个字典，字典里存储了所有图片的名称
    result = {}

    # 获取当前目录下所有的子目录
    sub_dirs = [x[0] for x in os.walk(INPUT_DATA)]
    # print(sub_dirs)
    # 得到的第一个目录是当前目录，不予考虑
    is_root_dir = True
    for sub_dir in sub_dirs:
        # print(sub_dir)
        if is_root_dir:
            is_root_dir = False
            continue
        dir_name = os.path.basename(sub_dir)
        label_name = dir_name.lower()
        result[label_name] = {
            'dir': dir_name,
        }
    return result



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

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=400, height=10)
        self.pack()
        self.File="C:\\Users\\Anzhi\Desktop\\first.png"
        self.pilImage = Image.open(self.File).resize((993,516))
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)

        self.path_label = tk.Label(self, text=self.File, width=100)
        self.path_label.pack()
        self.label = tk.Label(self, image=self.tkImage,width=993,height=516)
        self.label.pack()
        self.button=tk.Button(root, text='choose an image', command=self.printcoords,width=20).pack()
        self.pre_label=tk.Label(self,text='识别种类',width=100)
        self.pre_label.pack()


        ############################################################################################准备模型阶段,提高效率
        with tf.device('/cpu:0'):
            # 读取所有图片
            self.image_lists = create_image_lists();
            # 读取已经训练好的Inception-v3模型。
            with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
            print("YES")
            # 加载读取的Inception-v3模型，并返回数据输入所对应的张量以及计算瓶颈层结果所对应的张量
            self.bottleneck_tensor, self.jpeg_data_tensor = tf.import_graph_def(
                graph_def, return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])
            self.sess = tf.Session();
        self.saver = tf.train.import_meta_graph(".\\checkpoint_dir\\MyModel-10.meta");
        self.saver.restore(self.sess, tf.train.latest_checkpoint(".\\checkpoint_dir"));
        self.y = tf.get_collection("pred_network")[0]
        self.graph = tf.get_default_graph()
        self.input_x = self.graph.get_operation_by_name('BottleneckInputPlaceholder').outputs[0]
        ################################################################################################
    def predictDog(self):
        print("start")
        bottleneck = get_bottleneck(self.sess, self.File, self.jpeg_data_tensor, self.bottleneck_tensor);
        bottleneck = [float(x) for x in bottleneck]
        bottleneck = [bottleneck]
        p = self.sess.run(self.y, feed_dict={self.input_x: bottleneck});
        print(3)
        p = p[0];
        val, idx = max((val, idx) for (idx, val) in enumerate(p))
        label_name = list(self.image_lists.keys())[idx]
        return label_name, val * 100

    def processEvent(self, event):
        pass

        # function to be called when mouse is clicked
    def printcoords(self):
        try:
            self.File = filedialog.askopenfilename(parent=root, initialdir=".\\images", title='Choose an image.')
            self.path_label["text"]=self.File;

            label_name,val=self.predictDog()
            self.pilImage = Image.open(self.File);
            self.tkImage = ImageTk.PhotoImage(image=self.pilImage);
            self.pre_label["text"]=label_name+": {:.2f}%".format(val)
            self.label["image"]=self.tkImage
        except:
            pass



if __name__ == '__main__':
    root = tk.Tk()
    root.title("宠物狗识别系统")
    app = App(root)
    root.mainloop()
