function [ imgBin ] = ImageBin( img,sigma,volThreshold )
% funcition used for image preprocessing and binaryzation 
% sigma is parameters for multi-scale LOG filter
% volthreshold is used for delete small regions in binaryzation result 
% img is original image stack

% multi-scale LOG filer
imgBackGround=uint8(img);
for i=sigma(1):sigma(1)
    LOGResult=ImageFilter(img,i);
    imgBackGround=imgBackGround-LOGResult;
end
imgForeGround=img-imgBackGround;
% image binaryzation
imgBin=ImageThresh(imgForeGround);
imgBin(imgBin>0)=1;
imgBin=ImageVolEliminate(imgBin,volThreshold);
%fill the hole in imgBin
imgBin=imfill(imgBin,'holes');
end

