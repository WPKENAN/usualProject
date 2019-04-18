%读入图片
I=imread('5.png');
img=rgb2gray(I);

%均值滤波
H=ones(3,3)*0.111111;
img=imfilter(img,H,'same');
figure
imshow(img)
title('Mean-filter')

Prewitt=edge(img,'Prewitt',0.025);
figure
imshow(Prewitt);
title('Prewitt');

LOG=edge(img,'LOG',0.0015);
figure
imshow(LOG);
title('高斯-拉普拉斯')

Canny=edge(img,'Canny',0.025);
figure
imshow(Canny);
title('Canny')

Roberts=edge(img,'Roberts',0.022);
figure
imshow(Roberts);
title('Robert')

Sobel=edge(img,'Sobel',0.022);
figure
imshow(Sobel);
title('Sobel')


