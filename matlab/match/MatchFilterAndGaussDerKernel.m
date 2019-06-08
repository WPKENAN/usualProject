function [Kernel]  = MatchFilterAndGaussDerKernel(sigma,YLength,theta,type)
%
%    MF and FDOG construction
%               Inputs:
%                     sigma      -   scale value
%                     YLength    -   length of neighborhood along y-axis 
%                     theta      -   orientation（方向）
%                     type       -   MF or FDOG
%               Output:
%                     Kernel     -   Gaussian kernel
%
%               YLength should be an odd integer（奇整数）
%               this function is used to contruct the matchfilter kernel. sigma is used
%               for the Gaussian function.

% AUTHOR    Bob Zhang <yibo@pami.uwaterloo.ca>

% widthOfTheKernel = ceil(sqrt( (6*ceil(sigma)+1)^2 + YLength^2));
% if mod(widthOfTheKernel,2) == 0
%     widthOfTheKernel = widthOfTheKernel + 1;
% end
% 
% oneDimensionGauss = [];
% oneDimensionGaussDerivative = [];
% for i = -3*ceil(sigma):3*ceil(sigma)
%     oneDimensionGauss = [oneDimensionGauss -exp(-i^2/2/sigma^2)];
%     oneDimensionGaussDerivative = [oneDimensionGaussDerivative -exp(-i^2/2/sigma^2)*i/sigma^2];
% end
% 
% oneDimensionGauss = oneDimensionGauss - mean(oneDimensionGauss);
% realMatchFilterKernel = repmat(oneDimensionGauss,YLength,1);
% realGaussDerivativeKernel = repmat(oneDimensionGaussDerivative,YLength,1);
% %widthOfTheKernel = ceil (sqrt((3*ceil(sigma) + 1)^2 + YLength^2));
% matchFilterKernel = padarray(realMatchFilterKernel,[(widthOfTheKernel - YLength) / 2 (widthOfTheKernel- length(oneDimensionGauss))/2 ]);
% matchFilterKernel = imrotate(matchFilterKernel,theta,'nearest','crop');
% 
% GaussDerivativeKernel = padarray(realGaussDerivativeKernel,[(widthOfTheKernel - YLength) / 2 (widthOfTheKernel- length(oneDimensionGauss))/2 ]);
% GaussDerivativeKernel = imrotate(GaussDerivativeKernel,theta,'nearest','crop');
if type == 0
    widthOfTheKernel = ceil(sqrt( (6*ceil(sigma)+1)^2 + YLength^2));
    if mod(widthOfTheKernel,2) == 0
        widthOfTheKernel = widthOfTheKernel + 1;
    end
    halfLength = (widthOfTheKernel - 1) / 2;
    row = 1;
    for y = halfLength:-1:-halfLength
        col = 1;
        for x = -halfLength:halfLength
            xPrime = x * cos(theta) + y * sin(theta);
            yPrime = y * cos(theta) - x * sin(theta);
            if abs(xPrime)>3*ceil(sigma)
                matchFilterKernel(row,col) = 0;
            elseif abs(yPrime)> (YLength-1) / 2
                matchFilterKernel(row,col) = 0;
            else
                matchFilterKernel(row,col) = -exp(-.5*(xPrime/sigma)^2)/(sqrt(2*pi)*sigma); %%%%？？？？？
            end
            col = col + 1;
        end
        row = row + 1;
    end
    mean = sum(sum(matchFilterKernel)) / sum(sum(matchFilterKernel < 0));%%%会不会少了个2
    for i = 1:widthOfTheKernel
        for j =1:widthOfTheKernel
            if matchFilterKernel(i,j) < 0
                matchFilterKernel(i,j) = matchFilterKernel(i,j) - mean;
            end
        end
    end
    Kernel = matchFilterKernel;
else
    widthOfTheKernel = ceil(sqrt( (6*ceil(sigma)+1)^2 + YLength^2));
    if mod(widthOfTheKernel,2) == 0
        widthOfTheKernel = widthOfTheKernel + 1;
    end
    halfLength = (widthOfTheKernel - 1) / 2;
    row = 1;
    for y = halfLength:-1:-halfLength
        col = 1;
        for x = -halfLength:halfLength
            xPrime = x * cos(theta) + y * sin(theta);
            yPrime = y * cos(theta) - x * sin(theta);
            if abs(xPrime)>3*ceil(sigma)
                GaussDerivativeKernel(row,col)  = 0;
            elseif abs(yPrime)> (YLength-1) / 2
                GaussDerivativeKernel(row,col)  = 0;
            else
                GaussDerivativeKernel(row,col)= -exp(-.5*(xPrime/sigma)^2)*xPrime/(sqrt(2*pi)*sigma^3);
            end
            col = col + 1;
        end
        row = row + 1;
    end
    Kernel = GaussDerivativeKernel;
end 