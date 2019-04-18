figure
subplot(2,1,1)
plot(YTest)
hold on
plot(YPred,'.-')
hold off
legend(["Observed" "Forecast"])
ylabel("Price")
title("Forecast")

subplot(2,1,2)
stem(YPred - YTest)
xlabel("Hour")
ylabel("Error")
title("RMSE = " + rmse)