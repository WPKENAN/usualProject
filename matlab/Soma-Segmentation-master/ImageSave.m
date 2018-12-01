function ImageSave(image, path)
    % Save a 3D image stack
    disp(['save image to ' path]);
    [~, ~, depth] = size(image);
    imwrite(image(:, :, 1), path);
    for z = 2 : depth
        imwrite(image(:, :, z), path, 'writemode', 'append');
    end
end
