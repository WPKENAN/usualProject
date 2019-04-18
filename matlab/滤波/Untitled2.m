%¶ÁÈëÍ¼Æ¬
I=imread('2.png');
img=rgb2gray(I);

%¾ùÖµÂË²¨
H=ones(3,3)*0.111111;
img=filter2(H,img,'same')/255
figure
imshow(img)
title('Mean-filter')


img1=edge(img,'Roberts',0.02);
figure
imshow(img1);
title('Robert')


img2=edge(img,'Sobel',0.02);
figure
imshow(img2);
title('Sobel')

img3=edge(img,'Prewitt',0.02);
figure
imshow(img3);
title('Prewitt');

img4=edge(img,'LOG',0.001);
figure
imshow(img4);
title('LOG')

img5=edge(img,'Canny',0.02);
figure
imshow(img5);
title('Canny')
