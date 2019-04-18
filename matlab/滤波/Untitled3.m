%读入图片
I=imread('3.png');
image=rgb2gray(I);

%阈值
alpha=0.01

%均值滤波
H=fspecial('average',3)
image=conv2(image,H,'same')/255
figure
imshow(image)
title('Mean-filter')

image1=edge(image,'Roberts',alpha);
figure
imshow(image1);
title('Robert')


image2=edge(image,'Sobel',alpha);
figure
imshow(image2);
title('Sobel')

image3=edge(image,'Prewitt',alpha);
figure
imshow(image3);
title('Prewitt');

image4=edge(image,'LOG',alpha);
figure
imshow(image4);
title('LOG')

image5=edge(image,'Canny',alpha);
figure
imshow(image5);
title('Canny')
