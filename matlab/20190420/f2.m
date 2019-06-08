function f2(img)
    [x,y]=find(img==1);
    disp("灰度重心法的中心坐标位置是:");
    [sum(x)/length(x),sum(y)/length(y)]
end




