clc
clear
id = 101045451;clc
iteration = 0;

while id ~= 1
    if mod(id,2)==0
        iteration = iteration + 1;
        series(1,iteration) = id;
        id=id/2;
    else
        iteration = iteration + 1;
        series(1,iteration) = id;
        id=id*3+1;
    end
end

series(1,iteration + 1) = 1;

series = flip(series);

series = log10(series);

formatSpec = 'The number of iterations = %4.1f\n';
fprintf(formatSpec,iteration);
plot(series);
xlabel('x');
ylabel('y');
title('Gang Han-101030341')




    
