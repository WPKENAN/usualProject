 function [vess] = MatchFilterWithGaussDerivativeORSF(im,sigmaForMF,yLengthForMF,numOfDirections)
%
%    Retinal vessel extraction by matched filter with 
%    first-order derivative of Gaussian
%  
%               Inputs:
%                     k                  -   ignore, used for testing purposes only
%                     num                -   image number
%                     im                 -   input image
%                     sigmaForMF         -   scale value of MF
%                     sigmaForGD         -   scale value of FDOG
%                     yLengthForMF       -   length of neighborhood along y-axis of MF 
%                     yLengthForGD       -   length of neighborhood along y-axis of FDOG 
%                     tForMatchfilterRes -   threshold value of MF
%                     tForGaussDerRes    -   threshold value of FDOG
%                     numOfDirections    -   number of orientations
%                     mask               -   image mask
%                     maskForGDRange     -   another image mask
%                     c_value            -   c value
%                     t                  -   threshold value of MF-FDOG
% 
%               Output:
%                     vess     -   vessels extracted

% AUTHOR    Bob Zhang <yibo@pami.uwaterloo.ca>
% Modified by Wendeson Oliveira.

if isa(im,'double')~=1 
    im = double(im);
end

[rows,cols] = size(im);

MatchFilterRes(rows,cols,numOfDirections) = 0;


filtros = [];
for i = 0:numOfDirections-1
    matchFilterKernel = MatchFilterAndGaussDerKernel(sigmaForMF,yLengthForMF, pi/numOfDirections*i,1);
    filtros(:,:,i+1) = matchFilterKernel;
    MatchFilterRes(:,:,i+1) = conv2(im,matchFilterKernel,'same');
end

[vess] = max(MatchFilterRes,[],3);
