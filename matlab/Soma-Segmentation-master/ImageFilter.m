function imageg = ImageFilter(image,sigma)
    % multi-scale LoG filters
    type = class(image);
    image = double(image);    
    disp(['running LoG with sigma=',num2str(sigma)])

    w=round(3*sigma)*2+1;
    h=zeros(w,w,w,'double');
    [x,y,z]=ind2sub(size(h),1:numel(h));
    c=(w+1)/2;
    r=(x-c).^2+(y-c).^2+(z-c).^2;
    h(:)=(3-r/(sigma^2)).*exp(-r/(2*sigma^2));
    h = h./sum(abs(h(:)));
    %image=imfilter(image,h,'replicate');
    image=imfilter(image,h,'symmetric');
    imageg = feval(type, image./max(image(:)).*double(intmax(type)));
end