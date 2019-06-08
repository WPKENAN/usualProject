function f1(img)
    img=edge(img,'sobel', 0.09);
    imshow(img);
    [x,y]=find(img==1);

    ydata = y;
    xdata = x;

    k0 = ones(1,3);
    F = @(k)(xdata-k(1)).^2+(ydata-k(2)).^2-k(3)^2;
    [k,resnorm] = lsqnonlin(F,k0);

    %k(1)是圆心的x坐标
    %k(2)是圆心的y坐标
    %k(3)的绝对值是圆的半径
    
    figure
    r0 = [k(1),k(2)];
    R = abs(k(3));
    xx = k(1)-R:0.01*R:k(1)+R;
    y1_h = sqrt(R.^2 - (xx - r0(1)).^2) + r0(2);
    y2_h = -sqrt(R.^2 - (xx - r0(1)).^2) + r0(2);
    plot(xx,y1_h,'b');
    hold on;
    plot(xx,y2_h','b');
    plot(xdata,ydata,'*r');

    disp("圆形拟合的中心坐标位置是:");
    [k(1),k(2)]
end