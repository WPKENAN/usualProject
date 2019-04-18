%读入图片
I=imread('4.png');
img=rgb2gray(I);

%均值滤波
H=ones(3,3)*0.111111;
img=imfilter(img,H,'same')
figure
imshow(img)
title('Mean-filter')


img1=edge(img,'Prewitt',0.02);
figure
imshow(img1);
title('Prewitt');

img2=edge(img,'LOG',0.001);
figure
imshow(img2);
title('拉普拉斯')

img3=edge(img,'Canny',0.02);
figure
imshow(img3);
title('Canny')

img4=edge(img,'Roberts',0.02);
figure
imshow(img4);
title('Robert')

img5=edge(img,'Sobel',0.02);
figure
imshow(img5);
title('Sobel')


