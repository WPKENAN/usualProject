function [ imgFill,imgSize] = ImageBorderFill( img,imgSize,exSize )
% fill the border of image with zeros 
% exSize is Fill width  
imgSize=imgSize+2*exSize;
imgFill=zeros(imgSize);
imgFill(1+exSize:imgSize(1,1)-exSize,1+exSize:imgSize(1,2)-exSize,1+exSize:imgSize(1,3)-exSize)=img;
end

