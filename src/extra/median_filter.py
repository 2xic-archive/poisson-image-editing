
import numpy as np

#	https://en.wikipedia.org/wiki/Median_filter
def median_filter(image):
	results = image.copy()
	kernel_size = 3
	for y in range(image.shape[0]-kernel_size):
		for x in range(image.shape[1]-kernel_size):
			windowArea = image[y:y+kernel_size,
								x:x+kernel_size]
			median = np.median(windowArea)
			results[y, x] = median
	return results