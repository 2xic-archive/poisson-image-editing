import matplotlib.pyplot as plt
import blurring

image = blurring.blur("lena.png").fit(1)
plt.imshow(image, plt.cm.gray)
plt.show()

from PIL import Image
#img = Image.fromarray(image, 'RGB')
#img.show()
