function [consume,efficiency] = f3(~,~)
month = [1;2;3;4;5;6];
distance = [2445;2485;2115;2733;2084;2539];
fuel = [210;234;172;220;206;219];
title = {'Month','Distancekm','FuelL','MPG','Lper100km'};
SF = 3;
 
consume = fuel./(distance/100);
gfuel = fuel/3.785;
mdistance = distance/1.61;
efficiency = mdistance./gfuel;
consume = round(consume,SF, 'significant');
efficiency = round(efficiency,SF,'significant');
 
T = table(month,distance,fuel,efficiency,consume,'VariableNames',title)
 
formatSpec = 'The average fuel efficiency is %4.1f MPG\n';
fprintf(formatSpec,mean(efficiency))
formatSpec = 'The average fuel efficiency is %4.1f L/100km\n';
fprintf(formatSpec,mean(consume))
 
end
