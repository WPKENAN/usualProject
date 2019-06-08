figure
I = imread(".\simple_classes\0\my18.jpg");


%imshow(I)
%dsadasdad
imshow(I)
label = classify(net,I)

title(string(label) + ", " + num2str(100*max(probs(idx(i),:)),3) + "%");
