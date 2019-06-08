function [image2,MatchFilterKernel] = MatchFilter(image1,sigma,yLength, direction_number)

% sample:
%     sigma=[2.^(1/2), 2, 2*2.^(1/2), 4];
%     yLength=9;
%     direction_number=12;
%     for a=sigma
%         [MF,~] = MatchFilter(img, a, yLength,direction_number);
%         MF(mask==0) = 0;
%         MF = normalize(double(MF));
%         % Adding to features
%         features = cat(3, features, MF);
%     end
    
[a, b] = size(image1);
image1 = double(image1);
MatchFilter_image=zeros(a,b,direction_number);
for i = 1:direction_number
    MatchFilterKernel = MatchFilterAndGaussDerKernel(sigma,yLength, pi/direction_number*(i-1),0);
    MatchFilter_image(:,:,i) = conv2(image1,MatchFilterKernel,'same');
%     [x,y]=meshgrid(1:17,1:17);
%     mesh(x,y,MatchFilterKernel);
end
image2 = max(MatchFilter_image,[],3);
image2 = uint8(image2);

end

    