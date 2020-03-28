image_path = {
	'/Users/2xic/Desktop/NTNU/Andre semester/Fag/vitenskapelig programmering/imt3881-2020-prosjekt/hdr-bilder/Adjuster/Adjuster_00064.png' 
	'/Users/2xic/Desktop/NTNU/Andre semester/Fag/vitenskapelig programmering/imt3881-2020-prosjekt/hdr-bilder/Adjuster/Adjuster_00128.png' 
	'/Users/2xic/Desktop/NTNU/Andre semester/Fag/vitenskapelig programmering/imt3881-2020-prosjekt/hdr-bilder/Adjuster/Adjuster_00256.png' 
	'/Users/2xic/Desktop/NTNU/Andre semester/Fag/vitenskapelig programmering/imt3881-2020-prosjekt/hdr-bilder/Adjuster/Adjuster_00512.png' 
};
% as defined in the paper
B = [log(64) log(128) log(256) log(512)];

l = 100;


% loads the images
images = {
	

};
for img_number = 1: length(image_path)
    images{img_number} = imread(image_path{img_number});
end


% total pixel area
xy = size(images{1}, 1)*size(images{1}, 2);;


% get's the sample space
sample_size = 100;
sample_space = ceil(rand(1, sample_size)*xy);

%Z = zeros(sample_size, length(image_path), 3);
%gets the sample space
%for index = 1:length(image_path)
%    for channel = 0:2
%    	disp(images{index}(sample_space + (channel) * xy))
%        Z(:, index, channel+1) = images{index}(sample_space + (channel) * xy);
%    end
%end
load('Z.mat')
%save('/Users/2xic/Desktop/NTNU/Andre semester/Fag/vitenskapelig programmering/imt3881-2020-prosjekt/src/files/Z.mat','Z');


% gets the radiance form the gsolver
radiance = zeros(256, 3);
for channel = 1:3
    radiance(:, channel) = gsolve(Z(:,:,channel), B, l, @weigth, channel);
end
save 'matlab_radiance.mat' radiance 

% do the same for the rest of the function, we only check one here as a test.
figure
plot(radiance(:, 1), 'r');
title('R');

figure
plot(radiance(:, 2), 'g');
title('g');




