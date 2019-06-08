clc
clear
img=imread('C:\Users\Anzhi\Desktop\1.png');
img=rgb2gray(img);
subplot(2,2,1);imshow(img);title('原图')
subplot(2,2,2);imhist(img);title('原始图灰度直方图')
img=double(img);
size(img);
[m,n]=size(img);
A=reshape(img,m*n,1);
[label,C]=kmeans(A,3);

C;
rlabel=reshape(label,m,n);
[temp,index]=sort(C);



rGray=rlabel;
rGray(find(rlabel==index(1)))=0;
rGray(find(rlabel==index(2)))=128;
rGray(find(rlabel==index(3)))=255;
rGray=uint8(rGray);


subplot(2,2,3);imshow(rGray);title('分割图')
subplot(2,2,4);imhist(rGray);title('分割后的灰度直方图')
