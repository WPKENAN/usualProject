%id=101030341
clc
clear
y0=1;
w=4;
k=0.1;
y=[];
for t=-2:0.01:20
    if t<0
        y=[y,-y0];
    elseif t>=0 && t<10
        y=[y,-y0*cos(w*t)];
    else
        y=[y,-y0*cos(w*t)*exp(-k*(t-10))];
    end
end
plot([-2:0.01:20],y);
ylabel('y(t)')
xlabel('t/s')
title('Gang Han-101030341')
           
        