clc 
clear
path="D:\github\usualProject\matlab\20190420\1.png"
img=imread(path);
img=rgb2gray(img);
img=im2bw(img,0.90);

%%%方法一
f1(img);
%%%方法二
f2(img);





