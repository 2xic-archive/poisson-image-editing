from engine import hdr_image_handler
import matplotlib.pyplot as plt

x = hdr_image_handler.hdr_handler()


radiance = x.get_radiance()


for i in range(3):
	plt.subplot(3, 1, i + 1)
	plt.plot(radiance[:, i])
plt.show()
