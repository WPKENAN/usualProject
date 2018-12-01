function image = ImageEliminate(image, low)
    % Eliminate small regions in a 3D image stack
    disp(['image elimination with region size ' num2str(low)]);
    [lbl, num] = bwlabeln(image>0, 26);
    [reg, ~] = hist(lbl(lbl>0), 1:num);
    temp = image(lbl>0);
    temp(reg(lbl(lbl>0))<low) = 0;
    image(lbl>0) = temp;
end
