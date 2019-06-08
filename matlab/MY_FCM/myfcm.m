clc
clear
img=imread('C:\Users\Anzhi\Desktop\1.png');
img=rgb2gray(img);
subplot(2,2,1);imshow(img);title('原图')
subplot(2,2,2);imhist(img);title('原始图灰度直方图')
img=double(img);
size(img);
[m,n]=size(img);
data=reshape(img,m*n,1);

cluster_n=3
options = [2, 500, 1e-5, 0];   %设定聚类参数
[C, U, obj_fcn] = fcm(data, cluster_n, options); %调用fcm实现聚类， matlab自带
[~,label] = max(U); %找到所属的类

rlabel=reshape(label,m,n);
[temp,index]=sort(C);

rGray=rlabel;
rGray(find(rlabel==index(1)))=0;
rGray(find(rlabel==index(2)))=128;
rGray(find(rlabel==index(3)))=255;
rGray=uint8(rGray);

subplot(2,2,3);imshow(rGray);title('分割图')
subplot(2,2,4);imhist(rGray);title('分割后的灰度直方图')

