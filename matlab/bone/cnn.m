%划分训练集和测试集，训练集百分之70
[imdsTrain,imdsValidation] = splitEachLabel(imds,0.9);

%搭建网络
layers = [
    imageInputLayer(size(imread(imds.Files{1})))%输入层
    convolution2dLayer(3,10,'Padding','same')%第一个卷积层
    batchNormalizationLayer%局部归一化
    reluLayer%激活函数
    convolution2dLayer(3,10,'Padding','same')%2
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)%池化层
    
    convolution2dLayer(3,30,'Padding','same')%3
    batchNormalizationLayer
    reluLayer
    convolution2dLayer(3,30,'Padding','same')%4
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)

    fullyConnectedLayer(300)%全连接层
    reluLayer
    dropoutLayer(0.5)%随机失活，百分之50失活
    fullyConnectedLayer(numel(unique(imds.Labels)))%全连接层
    softmaxLayer%激活函数
    classificationLayer];
    layers(2).WeightL2Factor=0.002;%L2正则化
    layers(5).WeightL2Factor=0.002;
    
    layers(9).WeightL2Factor=0.002;
    layers(12).WeightL2Factor=0.002;

options = trainingOptions('adam', ...
    'InitialLearnRate',0.001, ...
    'MaxEpochs',10, ...
    'MiniBatchSize',64, ...
    'Shuffle','every-epoch', ...
    'ValidationData',imdsTrain, ...
    'ValidationFrequency',5, ...
    'Verbose',false, ...
    'Plots','training-progress');

disp('start train')
net = trainNetwork(imdsTrain,layers,options);%开始训练
analyzeNetwork(net)%输出网络

[YPred,probs] = classify(net,imdsValidation);%预测
YValidation = imdsValidation.Labels;%预测

%accuracy = sum(YPred == YValidation)/numel(YValidation)


%随机选9张图，预测一下
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
