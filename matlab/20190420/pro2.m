clc 
clear
path="D:\github\usualProject\matlab\20190420\2.png"
img=imread(path);
img=rgb2gray(img);
img=im2bw(img,0.90);
[m,n]=size(img);
xy=zeros(m,2);
imshow(img)
for i=1:m
    [x,y]=find(img(i,:)==1)
    xy(i,1)=i;
    xy(i,2)=sum(y)/length(y);
end

figure
disp("中心线位置是")
xy
path="D:\github\usualProject\matlab\20190420\2.png"
img=imread(path);
for i=1:m
    img(int16(xy(i,1)),int16(xy(i,2)),:)=[255,0,0];
end
imshow(img);
        
    