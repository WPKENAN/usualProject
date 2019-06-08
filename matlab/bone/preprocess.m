clc
clear
imds = imageDatastore('.\train', ...
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
     if length(size(image))==3
         image = rgb2gray(image);
     end
     imageDeel =imresize(image,[224,224]);
     delete(imds.Files{i})
     try
         imwrite(imageDeel,imds.Files{i});
     catch
         continue
     end
 end
dsadadsa
  for i = 1:length(imds.Files)
      image=imread(imds.Files{i});
      imds.Files{i}
      try
          if size(image)~=[224,224,3]
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
