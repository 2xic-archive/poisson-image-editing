from engine import hdr_image_handler
import matplotlib.pyplot as plt
import scipy.io

x = hdr_image_handler.hdr_handler()


radiance = x.get_radiance()

# Figure 7 in the paper
PLOT_RESPONSE_FUNCTIONS = False
if(PLOT_RESPONSE_FUNCTIONS):
	for i in range(3):
		plt.subplot(3, 1, i + 1)
		plt.plot(radiance[:, i])
	plt.show()

scipy.io.savemat('./files/rad.mat', dict(radiance=radiance))

exit(0)
import numpy as np

rad = x.get_radiance_log(radiance)
plt.imshow(rad)
plt.show()

scipy.io.savemat('test.mat', dict(rad=rad))

# normalize the image
for i in range(3):
	max_val = np.max(rad[:, :, i])
	min_vax = np.min(rad[:, :, i])
	print((max_val, min_vax))
	rad[:, :, i] = ((rad[:, :, i]) + abs(min_vax))/(max_val + abs(min_vax))

	max_val = np.max(rad[:, :, i])
	min_vax = np.min(rad[:, :, i])
	print((max_val, min_vax))
plt.imshow((255 * rad).astype(np.uint8))
plt.show()

