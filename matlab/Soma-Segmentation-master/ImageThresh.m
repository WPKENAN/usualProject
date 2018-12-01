function imageg = ImageThresh(image)
% OTSU thresholding
    type=class(image);
    level=graythresh(image);
    disp(['Bg intensity is ',num2str(level*intmax(type))]);
    imageg=image;
    imageg(image<level*intmax(type))=0;
end