clc 
clear
path="D:\github\usualProject\matlab\20190420\1.png"
img=imread(path);
img=rgb2gray(img);
img=im2bw(img,0.90);

%%%����һ
f1(img);
%%%������
f2(img);





