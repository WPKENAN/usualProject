import cv2 as cv
import numpy as np
from PIL import Image
import SimpleITK as sitk
from libtiff import TIFF




##图像序列保存成tiff文件
##image_dir：图像序列所在文件夹
##file_name：要保存的tiff文件名
##image_type:图像序列的类型
##image_num:要保存的图像数目
def image_array_to_tiff(image_dir, file_name, image_type, image_num):
    out_tiff = TIFF.open(file_name, mode='w')
    for i in range(0, image_num):
        image_name = image_dir+"//"+str(i) + image_type
        image_array = Image.open(image_name)
        # 缩放成统一尺寸
        img = image_array.resize((480, 480), Image.ANTIALIAS)
        out_tiff.write_image(img, compression=None, write_rgb=True)

if __name__=="__main__":
    image_dir="D:\github\Data\SARI\\test"
    file_name='test.tif'
    image_type=".png"
    image_num=43

    import os
    import shutil
    count=0;
    # for file in os.listdir(image_dir):
    #     shutil.copy(os.path.join(image_dir,file),os.path.join(image_dir,str(count)+".png"))
    #     count+=1
    image_array_to_tiff(image_dir, file_name, image_type, image_num)


