function [imgDist, somaLocations] = SomaLocate(imgBin,jitterHeight)
% imgBin indicates the binaryzation result of original image
% imgSize indicates the size of original image
% jitterHeight indicates the parameter of H-dome used for delete redundant soma centroids
% imgDist is distance tranform result of imgBin 
imgDist=bwdist(~imgBin);
imgDist=uint8(round(imgDist));% rounding the result of distance transformation 
[somaLocations,imgDist]=jitter(imgDist,jitterHeight);
end

