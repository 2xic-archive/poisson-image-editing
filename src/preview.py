import matplotlib.pyplot as plt
import blurring
import constrast

#image = constrast.contrast("lena.png").fit(1)#sobel()

#print(image)

from PIL import Image
image = blurring.blur("lena.png").fit(1)

print(image.data)
print(image.data.shape)

import numpy as np
img = Image.fromarray(np.uint8(image.data))#, 'RGB')


#plt.imshow(image.data / 255)#, plt.cm.gray)
#plt.show()

#print(image.data * 255)
img.show()
