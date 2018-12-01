function image = ImageLoad(path)
    % Load a 3D image stack
    disp(['load image from ' path]);
    depth = length(imfinfo(path));
    [height,width,channels] = size(imread(path));
    image = zeros(height, width, depth, 'uint8');
    if channels==3
        for z = 1 : depth
            tmp=rgb2gray(imread(path,z));
            image(:, :, z) = tmp;
        end
    else
        for z = 1 : depth
            image(:, :, z) = imread(path,z);
        end
    end
end
