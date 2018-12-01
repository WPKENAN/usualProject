function imageg = ImageVolEliminate(image,thr)
    [lbl,num]=bwlabeln(image,26);
    temp=lbl(lbl>0);    
    reg=hist(temp,num); 
    temp(reg(temp)<thr)=0; 
    imageg=image;
    lbl(lbl>0)=temp;   
    imageg(lbl==0)=0;
end