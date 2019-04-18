%ʵ�鲽��1����ȡ��ɫͼƬ
I=imread('1.png');%�����ɫͼƬ
I0=rgb2gray(I);%�Ѳ�ɫͼƬתΪ�Ҷ�ͼƬ��256��

%ʵ�鲽��2:�Լ�д��һ����ֵ�˲�����
n = 3;%�����˲����Ĵ�С
template = ones(n);%����һ��3x3��ȫ��1�ľ���
[height, width] = size(I0);%��ȡͼƬ�ĳ��Ϳ�
x1 = double(I0);%���������ͱ��double���͵�
x2 = x1;
for i = 1:height-n+1%��ѭ������ֵ�˲�
    for j = 1:width-n+1
        c = x1(i:i+n-1,j:j+n-1).*template;
        s = sum(sum(c));
        x2(i+(n-1)/2,j+(n-1)/2) = s/(n*n);
    end
end
g = uint8(x2);%���8λ���������� ���ֵ��256
subplot(231);%�ڵڶ��еĵ�һ�л�ͼ
imshow(g);title('��ֵ�˲�')%��ʾͼƬ

I0=g%��g��ֵ��I0

%ʵ�鲽��������ϵͳ�����Roberts��Ե��ⷽ�����б�Ե���
BW1=edge(I0,'Roberts',0.016);%����ϵͳԤ�����Roberts��Ե��⺯��
subplot(232);%�ڵ�һ�еڶ��л�ͼ
imshow(BW1);title('Robert���ӱ�Ե���')%��ʾͼƬ

%ʵ�鲽���ģ���ϵͳ�����Sobel��Ե��ⷽ�����б�Ե���
BW2=edge(I0,'Sobel',0.016);%����ϵͳԤ�����Sobel��Ե��⺯��
subplot(233);%�ڵ�һ�е����л�ͼ
imshow(BW2);title('Sobel���ӱ�Ե���')%��ʾͼƬ

%ʵ�鲽���壺��ϵͳ�����Prewitt��Ե��ⷽ�����б�Ե���
BW3=edge(I0,'Prewitt',0.016);%����ϵͳԤ�����Prewitt��Ե��⺯��
subplot(234);%�ڵڶ��е�һ�л�ͼ
imshow(BW3);title('Prewitt���ӱ�Ե���');%��ʾͼƬ

%ʵ�鲽��������ϵͳ�����LOG��Ե��ⷽ�����б�Ե���
BW4=edge(I0,'LOG',0.001);%����ϵͳԤ�����LOG��Ե��⺯��
subplot(235);%�ڵڶ��еڶ��л�ͼ
imshow(BW4);title('LOG���ӱ�Ե���')%��ʾͼƬ

%ʵ�鲽���ߣ���ϵͳ�����Canny��Ե��ⷽ�����б�Ե���
BW5=edge(I0,'Canny',0.02);%����ϵͳԤ�����Canny��Ե��⺯��
subplot(236);%�ڵڶ��е����л�ͼ
imshow(BW5);title('Canny���ӱ�Ե���')%��ʾͼƬ
