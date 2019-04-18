function f1(x,y);
    x1 = size(x);
    y1 = size(y);

    if x1(:,1) == 1
        x = x';
    end

    if y1(:,1) == 1
        y = y';
    end

    if length(x) == length(y)
        output = x.*(y.^2);
        T = table(x,y,output,'VariableNames',{'x' 'y' 'output'})
    else
        disp('Your vectors are not the same length')
    end
end
