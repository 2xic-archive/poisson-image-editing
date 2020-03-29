from experimental import implicit
from backend import blurring
from experimental import implicit_inpait
from backend import inpaiting
from backend import blurring
from PIL import Image
from engine import hdr_image_handler
import matplotlib.pyplot as plt
import numpy as np


x = hdr_image_handler.hdr_handler()

radiance = x.get_radiance()

#plt.plot(radiance[:, 0])
#plt.show()


radiance_log = x.get_radiance_log(radiance)
print(radiance_log.shape)

def normalize(x):
	# rgb
	for i in range(x.shape[-1]):
		max_val = np.max(x[:, :, i])
		min_val = np.min(x[:, :, i])
		x[:, :, i] = (x[:, :, i] + abs(min_val))/(max_val + abs(min_val))
	return x

plt.imshow(normalize(radiance_log))
plt.show()

exit(0)


#print(x.images)

#for i in x.images:
#	i.show()
#	im = Image.open(i.path)
#	width, height = im.size
#	im = im.resize((width//scale, height//scale))
#	im.show()  


'''
#x = implicit.blur("./files/test_images/lena.png")
y = implicit_inpait.inpaint("./files/test_images/lena.png")
x = inpaiting.inpaint("./files/test_images/lena.png")

x.data = y.data.copy()
x.mask = y.mask.copy()
x.original_data = y.original_data.copy()

y.fit(epochs=10)
y.save("./experimental/results/implicit.png")


x.fit(epochs=10)
x.save("./experimental/results/explicit.png")
'''

#x.show()

'''
y = blurring.blur("./files/test_images/lena.png")
y.fit(500)
y.show()

print("hei")

y.fit(1000)
y.show()
'''

'''
print((x.data - y.data).sum())
'''