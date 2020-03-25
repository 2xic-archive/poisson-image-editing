import numpy as np


#	https://en.wikipedia.org/wiki/Median_filter
def median_filter(image):
    """
	Preform median filter on image

	Parameters
	----------
	image : ndarray
		The image to preform the filter on
	"""
    results = image.copy()
    kernel_size = 3
    for y in range(image.shape[0] - kernel_size):
        for x in range(image.shape[1] - kernel_size):
            window_area = image[y:y + kernel_size,
                          x:x + kernel_size]
            median = np.median(window_area)
            results[y, x] = median
    return results
