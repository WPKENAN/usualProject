clc 
clear
path="D:\github\usualProject\matlab\20190420\3.png"
img=imread(path);
img=rgb2gray(img);

figure;
subplot(131);
imshow(img);title('ԭͼ');
% ��ԭͼ��ƽ���ݶ�
imxy=edge(img,'sobel');
s1 = mean(imxy(:))

% ��1�θ�˹ģ����ͼ���ƽ���ݶ�
f1 = fspecial('gaussian',25,25);
img1 =imfilter(img,f1,'replicate');
imxy=edge(img1,'sobel');
s2 = mean(imxy(:))
subplot(132);imshow(img1);title('һ�θ�˹ģ��');

% ��2�θ�˹ģ����ͼ���ƽ���ݶ�
f2 = fspecial('gaussian',25,25);
img2 =imfilter(img1,f2,'replicate');
imxy=edge(img2,'sobel');
s3 = mean(imxy(:))
subplot(133);imshow(img2);title('2�θ�˹ģ��');
