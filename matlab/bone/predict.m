figure
%I = imread(".\train\negative\N626.png");
I = imread(".\N1.png");
imshow(I)


if length(size(I))==3
         I = rgb2gray(I);
end
I=imresize(I,[224,224]);

[label,probs]= classify(net,I)%�������磬Ԥ��һ��

title(string(label) + ", " + num2str(100*max(probs),3) + "%");
