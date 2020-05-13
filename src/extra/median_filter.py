import numpy as np


#	https://en.wikipedia.org/wiki/Median_filter
def median_filter(image, mask):
    """
	Preform median filter on image

	Parameters
	----------
	image : ndarray
		The image to preform the filter on
    mask : ndarray
        Where to apply the median filter

    Returns
    -------
    ndarray
        The image with a median filter applied
	"""
    kernel_size = 3
    switch_back = False
    if len(image.shape) == 2:
        image = image.reshape(image.shape + (1,))
        switch_back = True

    results = image.copy()
    for z in range(image.shape[2]):
        for y in range(image.shape[0] - kernel_size):
            for x in range(image.shape[1] - kernel_size):
                window_area = image[y:y + kernel_size,
                              x:x + kernel_size, z]
                median = np.median(window_area)
                results[y, x, z] = median
    image[~mask.astype(bool)] = results[~mask.astype(bool)]

    if switch_back:
        image = image[:, :, 0]
    return image
