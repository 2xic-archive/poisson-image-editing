#from gui.interfaces import blurring_qt
import time
import sys
sys.path.append("./")
from engine import image_handler

# https://stackoverflow.com/a/5478448
def timing(f):
	def wrap(*args):
		time1 = time.time()
		ret = f(*args)
		time2 = time.time()
		print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
		return ret
	return wrap

from PIL import Image
from rapport_snippets.figs import *
from backend import blurring
import scipy
import scipy.ndimage
import scipy.misc
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow
import numpy as np
from scipy import ndimage


# http://www.adeveloperdiary.com/data-science/computer-vision/applying-gaussian-smoothing-to-an-image-using-python-from-scratch/
def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)

def gaussian_kernel(size, sigma=1, verbose=False):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)
    kernel_2D *= 1.0 / kernel_2D.max()
 
    if verbose:
        plt.imshow(kernel_2D, interpolation='none', cmap='gray')
        plt.title("Kernel ( {}X{} )".format(size, size))
        plt.show()
 
    return kernel_2D

@timing
def test_blur_filter():
	blurring_obj = blurring.blur("./files/test_images/lena.png", False)
	image = blurring_obj.data
	kernel = gaussian_kernel(3, sigma=1)

	image_row, image_col = image.shape
	kernel_row, kernel_col = kernel.shape
	 
	output = np.zeros(image.shape)
	 
	pad_height = int((kernel_row - 1) / 2)
	pad_width = int((kernel_col - 1) / 2)
	 
	padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))
	padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image

	print(np.max(padded_image))
	for row in range(image_row):
		for col in range(image_col):
			output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])#.clip(0, 1)
#	image = image_handler.ImageHandler(None, False)
#	image.data = np.uint8(output * 255)
#	image.save("test.jpg")
	from PIL import Image
	Image.fromarray(np.uint8(output * 255).astype(np.uint32)).convert("RGB").save("test.png")

#	plt.imshow(output, cmap='gray')
#	plt.show()

@timing
def test_blur_poision():
	blurring_obj = blurring.blur("./files/test_images/lena.png", False)
	blurring_obj.fit(50)
	#blurring_obj.show()


def compile(output_path="./rapport_snippets/output/glatting/"):
	color = True
	epoch_count = {
		0.5:[3, 5, 10],
		0.75:[3, 5, 10]
	}
	for color in [True, False]:
	#        self.mode_poisson = self.EXPLICIT 0
	#        self.mode_poisson = self.IMPLICIT 1
		for numeric in [0, 1]:
			blurring_obj = blurring.blur("./files/test_images/lena.png", color)
			blurring_obj.mode_poisson = numeric

			naming = "_color" if color else "_gray"
			naming += "_explicit" if blurring_obj.mode_poisson == 0 else "_implicit"

			if not os.path.isdir("{}/blur{}/".format(output_path, naming)):
				os.mkdir("{}/blur{}/".format(output_path, naming))

			results_doc = compile_doc(blurring_obj, epoch_count, "{}/blur{}/".format(output_path, naming), 
				"glatting/blur{}".format(naming))
			results_doc.save("{}/blur{}/results.tex".format(output_path,naming))

if __name__ == "__main__":
	test_blur_filter()












