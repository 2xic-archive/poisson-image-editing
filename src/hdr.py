from engine import hdr_image_handler
import matplotlib.pyplot as plt

x = hdr_image_handler.hdr_handler()


radiance = x.get_radiance()

#print(radiance)
plt.plot(radiance[:, 0])
plt.show()
