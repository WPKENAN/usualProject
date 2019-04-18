function [posr,posc]=Harris1(in_image,a)
% ���ܣ����ͼ��harris�ǵ�
% in_image-������rgbͼ������
% a--�ǵ������Ӧ��ȡֵ��Χ��0.04~0.06
% [posr��posc]-�ǵ�����
%in_image=rgb2gray(in_image);
I=double(in_image);
%%%%����xy�����ݶ�%%%%%
fx=[-1,0,1];%x�����ݶ�ģ��
Ix=filter2(fx,I);%x�����˲�
fy=[-1;0;1];%y�����ݶ�ģ��(ע���Ƿֺ�)
Iy=filter2(fy,I);
%%%%�������������ݶȵĳ˻�%%%%%
Ix2=Ix.^2;
Iy2=Iy.^2;
Ixy=Ix.*Iy;
%%%%ʹ�ø�˹��Ȩ�������ݶȳ˻����м�Ȩ%%%%
%����һ��7*7�ĸ�˹��������sigmaֵΪ2
h=fspecial('gaussian',[3,3],2);
IX2=filter2(h,Ix2);
IY2=filter2(h,Iy2);
IXY=filter2(h,Ixy);
%%%%%����ÿ����Ԫ��Harris��Ӧֵ%%%%%
[height,width]=size(I);
R=zeros(height,width);
%����(i,j)����Harris��Ӧֵ
for i=1:height
    for j=1:width
        M=[IX2(i,j) IXY(i,j);IXY(i,j) IY2(i,j)];
        R(i,j)=det(M)-a*(trace(M))^2;
    end
end
%%%%%ȥ��С��ֵ��Harrisֵ%%%%%
Rmax=max(max(R));
%��ֵ
t=0.005*Rmax;
for i=1:height
    for j=1:width
        if R(i,j)<t
            R(i,j)=0;
        end
    end
end
%%%%%����3*3����Ǽ���ֵ����%%%%%%%%%
corner_peaks=imregionalmax(R);
%imregionalmax�Զ�άͼƬ������8����Ĭ�ϣ�Ҳ��ָ�������Ҽ�ֵ����άͼƬ����26����
%��ֵ��Ϊ1��������Ϊ0
num=sum(sum(corner_peaks));
%%%%%%��ʾ����ȡ��Harris�ǵ�%%%%
[posr,posc]=find(corner_peaks==1);
figure;
imshow(uint8(in_image));
hold on
for i=1:length(posr)
    plot(posc(i),posr(i),'r+');
end
end