clc
clear
imds = imageDatastore('.\simple_classes', ...
    'IncludeSubfolders',true, ...
    'LabelSource','foldernames'); 

%figure;
%perm = randperm(75,10);
 for i = 1:length(imds.Files)
     %subplot(2,5,i);
     imds.Files{i}
     try
        image=imread(imds.Files{i});
     catch
         delete(imds.Files{i})
     end
     imageDeel =imresize(image,[128,128]);
     delete(imds.Files{i})
     try
         imwrite(imageDeel,imds.Files{i});
     catch
         continue
     end
 end

  for i = 1:length(imds.Files)
      image=imread(imds.Files{i});
      imds.Files{i}
      try
          if size(image)~=[256,256,3]
              imds.Files{i}
          end
      catch
          delete(imds.Files{i})
      end
     %subplot(2,5,i);
     %imds.Files{i}
     %image=imread(imds.Files{i});
     %imageDeel =imresize(image,[256,256]);
     %delete(imds.Files{i})
     %imwrite(imageDeel,imds.Files{i});
     %imshow(imds.Files{perm(i)});
  end
clc
clear
imds = imageDatastore('D:\github\usualProject\matlab\acc90\simple_classes', ...
    'IncludeSubfolders',true, ...
    'LabelSource','foldernames'); 