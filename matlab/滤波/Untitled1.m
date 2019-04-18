%实验步骤1：读取彩色图片
I=imread('1.png');%读入彩色图片
I0=rgb2gray(I);%把彩色图片转为灰度图片，256级

%实验步骤2:自己写的一个均值滤波函数
n = 3;%定义滤波器的大小
template = ones(n);%生成一个3x3的全是1的矩阵
[height, width] = size(I0);%获取图片的长和宽
x1 = double(I0);%将数据类型变成double类型的
x2 = x1;
for i = 1:height-n+1%做循环，均值滤波
    for j = 1:width-n+1
        c = x1(i:i+n-1,j:j+n-1).*template;
        s = sum(sum(c));
        x2(i+(n-1)/2,j+(n-1)/2) = s/(n*n);
    end
end
g = uint8(x2);%变成8位的数据类型 最大值是256
subplot(231);%在第二行的第一列画图
imshow(g);title('均值滤波')%显示图片

I0=g%把g赋值给I0

%实验步骤三：用系统定义的Roberts边缘检测方法进行边缘检测
BW1=edge(I0,'Roberts',0.016);%调用系统预定义的Roberts边缘检测函数
subplot(232);%在第一行第二列画图
imshow(BW1);title('Robert算子边缘检测')%显示图片

%实验步骤四：用系统定义的Sobel边缘检测方法进行边缘检测
BW2=edge(I0,'Sobel',0.016);%调用系统预定义的Sobel边缘检测函数
subplot(233);%在第一行第三列画图
imshow(BW2);title('Sobel算子边缘检测')%显示图片

%实验步骤五：用系统定义的Prewitt边缘检测方法进行边缘检测
BW3=edge(I0,'Prewitt',0.016);%调用系统预定义的Prewitt边缘检测函数
subplot(234);%在第二行第一列画图
imshow(BW3);title('Prewitt算子边缘检测');%显示图片

%实验步骤六：用系统定义的LOG边缘检测方法进行边缘检测
BW4=edge(I0,'LOG',0.001);%调用系统预定义的LOG边缘检测函数
subplot(235);%在第二行第二列画图
imshow(BW4);title('LOG算子边缘检测')%显示图片

%实验步骤七：用系统定义的Canny边缘检测方法进行边缘检测
BW5=edge(I0,'Canny',0.02);%调用系统预定义的Canny边缘检测函数
subplot(236);%在第二行第三列画图
imshow(BW5);title('Canny算子边缘检测')%显示图片
