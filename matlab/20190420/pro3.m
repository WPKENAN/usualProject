clc 
clear
path="D:\github\usualProject\matlab\20190420\3.png"
img=imread(path);
img=rgb2gray(img);

figure;
subplot(131);
imshow(img);title('原图');
% 求原图的平均梯度
imxy=edge(img,'sobel');
s1 = mean(imxy(:))

% 求1次高斯模糊后图像的平均梯度
f1 = fspecial('gaussian',25,25);
img1 =imfilter(img,f1,'replicate');
imxy=edge(img1,'sobel');
s2 = mean(imxy(:))
subplot(132);imshow(img1);title('一次高斯模糊');

% 求2次高斯模糊后图像的平均梯度
f2 = fspecial('gaussian',25,25);
img2 =imfilter(img1,f2,'replicate');
imxy=edge(img2,'sobel');
s3 = mean(imxy(:))
subplot(133);imshow(img2);title('2次高斯模糊');
