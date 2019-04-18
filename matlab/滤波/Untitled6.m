%读入图片并转为黑白
I=imread('6.png');
image=rgb2gray(I);

%均值滤波
n = 3;
template = ones(n);
[height, width] = size(image);
x1 = double(image);
x2 = x1;
for i = 1:height-n+1
    for j = 1:width-n+1
        c = x1(i:i+n-1,j:j+n-1).*template;
        s = sum(sum(c));
        x2(i+(n-1)/2,j+(n-1)/2) = s/(n*n);
    end
end


image = uint8(x2);
figure
imshow(image)
title('均值滤波')


Prewitt=edge(image,'Prewitt',0.025);
figure
imshow(Prewitt);
title('Prewitt');

LOG=edge(image,'LOG',0.0015);
figure
imshow(LOG);
title('高斯-拉普拉斯')

Canny=edge(image,'Canny',0.025);
figure
imshow(Canny);
title('Canny')

Roberts=edge(image,'Roberts',0.022);
figure
imshow(Roberts);
title('Robert')

Sobel=edge(image,'Sobel',0.022);
figure
imshow(Sobel);
title('Sobel')