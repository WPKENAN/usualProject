

[imdsTrain,imdsValidation] = splitEachLabel(imds,0.99);

layers = [
    imageInputLayer(size(imread(imds.Files{1})))
    
    
    convolution2dLayer(9,50,'Padding','same')
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)
    %dropoutLayer(0.5)
    
    convolution2dLayer(5,20,'Padding','same')
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)
    dropoutLayer(0.5)
    
    %fullyConnectedLayer(500)
    %reluLayer
    
    fullyConnectedLayer(numel(unique(imds.Labels)))
    softmaxLayer
    classificationLayer];
%layers(2).WeightL2Factor=10;
%layers(7).WeightL2Factor=10;

options = trainingOptions('adam', ...
    'InitialLearnRate',0.001, ...
    'MaxEpochs',50, ...
    'MiniBatchSize',64, ...
    'Shuffle','every-epoch', ...
    'ValidationData',imdsValidation, ...
    'ValidationFrequency',5, ...
    'Verbose',false, ...
    'Plots','training-progress');

disp('start train')
net = trainNetwork(imdsTrain,layers,options);
analyzeNetwork(net)

[YPred,probs] = classify(net,imdsValidation);
YValidation = imdsValidation.Labels;

accuracy = sum(YPred == YValidation)/numel(YValidation)



showNum=min(numel(imdsValidation.Files),9)
idx = randperm(numel(imdsValidation.Files),showNum);
figure
for i = 1:showNum
    subplot(3,3,i)
    I = readimage(imdsValidation,idx(i));
    imshow(I)
    label = YPred(idx(i));
    title(string(label) + ", " + num2str(100*max(probs(idx(i),:)),3) + "%");
end
