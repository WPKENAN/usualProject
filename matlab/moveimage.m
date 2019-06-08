clc
clear
srcFolder='.\images'
targetFolder='.\targetFolder'

files=dir(srcFolder)

count=-1;
interval=1
for i=1:length(files)
    if files(i).isdir==0
        count=count+1
        if mod(count,interval)==0
            copyfile([files(i).folder,'\',files(i).name],[targetFolder,'\',files(i).name])
        end
    end
end
%copyfile(filename,DST_PATH_t);


