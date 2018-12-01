function [regionalmax,dt] = jitter(dt,jitterh)
maxdt=double(imregionalmax(dt));
dt=double(dt);
if jitterh>0
    dt0=dt;
    rm=cell(jitterh+1,1);
    for i=1:(jitterh+1)
        if(max(dt(:))==0)
            rm{i}=zeros(size(dt));
        else
            rm{i}=double(imregionalmax(dt));
        end
        dt=dt-rm{i};
    end
    dt=dt+rm{i};
    regionalmax=rm{1};
    for i=1:jitterh
        regionalmax=regionalmax.*rm{i+1};
    end
    dt0(dt<=0)=0;
    maxdt=maxdt-regionalmax;
    re0=dt.*maxdt;
    or0=1-maxdt;
    or=dt0.*or0;
    dt=re0+or;
elseif jitterh==0
    regionalmax=imregionalmax(dt);
else
    disp('Wrong jitter value.');
    return
end
end



