function WriteSwc (vectors,filename)
    n=length(vectors(:,1));   
    tmp=vectors(:,2);
    vectors(:,2)=vectors(:,1);
    vectors(:,1)=tmp;
    %apo2swc
    cen=vectors;
    fid=fopen(filename,'w');
    k=1;
    for i=1:length(cen(:,1))
        for j=1:8
            if j==8
                fprintf(fid,'\n');
            elseif j==1
                fprintf(fid,'%d,',k);
                k=k+1;
            elseif j==2 || j==6
                fprintf(fid,'%d,',0);
            elseif j>2 &&j<6
                fprintf(fid,'%f,',cen(i,j-2));
            elseif j==7
                fprintf(fid,'%d,',-1);
            end
        end
    end

    fclose(fid);
end