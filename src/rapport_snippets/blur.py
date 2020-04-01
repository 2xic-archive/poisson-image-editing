#from gui.interfaces import blurring_qt
import time

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
	#face = imread("./files/test_images/lena.png")
	blurring_obj = blurring.blur("./files/test_images/lena.png", False)
	image = blurring_obj.data
	#blurred_face = scipy.ndimage.gaussian_filter(face, sigma=3)
	kernel = gaussian_kernel(3, sigma=52)
#	print(x.shape)
#	print(face.sh)
#	ndimage.convolve2d(face, x, mode='nearest')
#	imshow(scipy.ndimage.convolve(face, x, mode='nearest'))
#	plt.show()
	image_row, image_col = image.shape
	kernel_row, kernel_col = kernel.shape
	 
	output = np.zeros(image.shape)
	 
	pad_height = int((kernel_row - 1) / 2)
	pad_width = int((kernel_col - 1) / 2)
	 
	padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))
	padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image

#	for i in range(4):
	if(False):
		for row in range(image_row):
			for col in range(image_col):
				output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])#.clip(0,1)
#		padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = out

	output = scipy.ndimage.gaussian_filter(image, sigma=5)

#	imshow(output, cmap='gray')#scipy.ndimage.convolve(image, x, mode='nearest'))
#	plt.show()


@timing
def test_blur_poision():
	blurring_obj = blurring.blur("./files/test_images/lena.png", False)
	blurring_obj.fit(50)
	#blurring_obj.show()

#test_blur_poision()
#test_blur_filter()

#imshow(very_blurred)
#plt.show()


def compile():
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

			if not os.path.isdir("./rapport_snippets/output/blur{}/".format(naming)):
				os.mkdir("./rapport_snippets/output/blur{}/".format(naming))

			results_doc = compile_doc(blurring_obj, epoch_count, "./rapport_snippets/output/blur{}/".format(naming), "glatting/blur{}".format(naming))
			results_doc.save("rapport_snippets/output/blur{}/results.tex".format(naming))


#if(color):
#	results_doc = compile_doc(blurring_obj, epoch_count, "./rapport_snippets/output/blur_color/", "glatting/blur_color")
#	results_doc.save("rapport_snippets/output/blur_color/results.tex")
#else:
#	results_doc = compile_doc(blurring_obj, epoch_count, "./rapport_snippets/output/blur/", "glatting/blur")
#	results_doc.save("rapport_snippets/output/blur/results.tex")













