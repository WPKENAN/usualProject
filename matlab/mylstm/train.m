%data = chickenpox_dataset;
function [net,pre]=train(data,team,days)
    
    
    figure(1)
    set(figure(1),'visible','off');
    plot(data)
    xlabel("The number of a play")
    ylabel("Score")
    title("team\_"+team+"-Score\_No")
    saveas(1,".\result\team_"+team+"-Score_No.jpg")
    %numTimeStepsTrain = floor(0.95*numel(data));
    numTimeStepsTrain=95-5;
    %numTimeStepsTrain=length(priceTrain)

    dataTrain = data(1:numTimeStepsTrain);
    dataTest = data(numTimeStepsTrain+1:end);

    mu = mean(dataTrain);
    sig = std(dataTrain);

    dataTrainStandardized = (dataTrain - mu) / sig;

    XTrain = dataTrainStandardized(1:end-12);
    YTrain = dataTrainStandardized(13:end);

    numFeatures = 1;
    numResponses = 1;
    numHiddenUnits = 400;

    layers = [ ...
        sequenceInputLayer(numFeatures)
        lstmLayer(numHiddenUnits)
        fullyConnectedLayer(numResponses)
        regressionLayer];

    options = trainingOptions('adam', ...
        'MaxEpochs',400, ...
        'GradientThreshold',1, ...
        'InitialLearnRate',0.005, ...
        'LearnRateSchedule','piecewise', ...
        'LearnRateDropPeriod',100, ...
        'LearnRateDropFactor',0.2, ...
        'Verbose',0, ...
        'Plots','training-progress');

    net = trainNetwork(XTrain,YTrain,layers,options);
    
    dataTestStandardized = (dataTest - mu) / sig;
    XTest = dataTestStandardized(1:end-1);
    net = predictAndUpdateState(net,XTrain);
    [net,YPred] = predictAndUpdateState(net,YTrain(length(YTrain)));

    numTimeStepsTest = numel(XTest);

    for i = 2:numTimeStepsTest
        [net,YPred(:,i)] = predictAndUpdateState(net,YPred(:,i-1),'ExecutionEnvironment','cpu');
    end
    YPred = sig*YPred + mu
    YTest = dataTest(2:end);
    rmse = sqrt(mean((YPred-YTest).^2))
    figure(2)
    set(figure(2),'visible','off');
    plot(dataTrain(1:end-1))
    hold on
    idx = numTimeStepsTrain:(numTimeStepsTrain+numTimeStepsTest);
    plot(idx,[data(numTimeStepsTrain) YPred],'.-')
    hold off
    xlabel("The number of a play")
    ylabel("Score")
    title("Forecast")
    legend(["Observed" "Forecast"])
    saveas(2,".\result\team_"+team+"-Forecast.jpg")
    
    figure(3)
    set(figure(3),'visible','off');
    subplot(2,1,1)
    plot(YTest)
    hold on
    plot(YPred,'.-')
    hold off
    legend(["Observed" "Forecast"])
    xlabel("The number of a play")
    ylabel("Score")

    subplot(2,1,2)
    stem(YPred - YTest)
    xlabel("The number of a play")
    ylabel("Error")
    title("RMSE = " + rmse)
    saveas(3,".\result\team_"+team+"-RMSE.jpg")
    
    %Ô¤²âdaysÌì
    dataTestStandardized = (dataTest - mu) / sig;
    XTest = dataTestStandardized(1:end-1);
    net = predictAndUpdateState(net,XTrain);
    [net,YPred] = predictAndUpdateState(net,YTrain(length(YTrain)));

    numTimeStepsTest = numel(XTest);

    for i = 2:numTimeStepsTest+days
        [net,YPred(:,i)] = predictAndUpdateState(net,YPred(:,i-1),'ExecutionEnvironment','cpu');
    end
    YPred = sig*YPred + mu
    pre=YPred(length(YPred)-days+1:length(YPred));
   
end
