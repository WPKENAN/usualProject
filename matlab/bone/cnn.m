%����ѵ�����Ͳ��Լ���ѵ�����ٷ�֮70
[imdsTrain,imdsValidation] = splitEachLabel(imds,0.9);

%�����
layers = [
    imageInputLayer(size(imread(imds.Files{1})))%�����
    convolution2dLayer(3,10,'Padding','same')%��һ�������
    batchNormalizationLayer%�ֲ���һ��
    reluLayer%�����
    convolution2dLayer(3,10,'Padding','same')%2
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)%�ػ���
    
    convolution2dLayer(3,30,'Padding','same')%3
    batchNormalizationLayer
    reluLayer
    convolution2dLayer(3,30,'Padding','same')%4
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2,'Stride',2)

    fullyConnectedLayer(300)%ȫ���Ӳ�
    reluLayer
    dropoutLayer(0.5)%���ʧ��ٷ�֮50ʧ��
    fullyConnectedLayer(numel(unique(imds.Labels)))%ȫ���Ӳ�
    softmaxLayer%�����
    classificationLayer];
    layers(2).WeightL2Factor=0.002;%L2����
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
net = trainNetwork(imdsTrain,layers,options);%��ʼѵ��
analyzeNetwork(net)%�������

[YPred,probs] = classify(net,imdsValidation);%Ԥ��
YValidation = imdsValidation.Labels;%Ԥ��

%accuracy = sum(YPred == YValidation)/numel(YValidation)


%���ѡ9��ͼ��Ԥ��һ��
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
