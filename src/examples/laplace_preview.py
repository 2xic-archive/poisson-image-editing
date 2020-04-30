

import sys
sys.path.append('./')

from engine import image_handler# import *
from engine.poisson import *

import matplotlib.pyplot as plt


photo = image_handler.ImageHandler("./files/test_images/lena.png", False)
po = poisson()


f, axarr = plt.subplots(2)

axarr[0].imshow(po.get_laplace_explicit(photo.data, alpha=False))
axarr[1].imshow(po.get_laplace_implicit(photo.data))
#axarr[0,1].imshow(image_datas[1])


plt.show()