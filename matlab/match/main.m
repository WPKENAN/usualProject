clc
clear
imagePath='D:\wp\Download\match\image\5944_right.jpeg'
sigma=2;
yLength=9;
direction_number=12;
img=imread(imagePath);
[org_x,org_y,org_c]=size(img)

img=imresize(img,[512,ceil(org_y/org_x*512+0.5)],'bicubic');
img=rgb2gray(img);


figure
subplot(1,2,1)
imshow(img);

MF = MatchFilter(img, sigma, yLength,direction_number);
MF = normalize(double(MF));
% Adding to features
features = MF;
subplot(1,2,2)
imshow(features)
