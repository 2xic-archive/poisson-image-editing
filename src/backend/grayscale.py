from engine import image_handler
import numpy as np
from engine import poisson
from engine import boundary

class grayscale(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a grayscaled image.

	This contains all the functions needed to make a color image into a grayscaled image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""
	def __init__(self, path, color=True):
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		boundary.Boundary.__init__(self)

		self.alpha = 0.25

		self.avg = self.data.copy().mean(axis=2)
		self.h = self.h()
		self.results = np.zeros((self.data.shape[:2]))

	def h(self):
		# TODO : Remove need for scipy
		from scipy import ndimage
		sx = ndimage.sobel(self.data, axis=0, mode='constant')
		sy = ndimage.sobel(self.data, axis=1, mode='constant')

		g = np.sum(np.sqrt(sx ** 2 + sy ** 2) / np.sqrt(3))

		rgb_gradient = np.sum(self.data[:, :, 0] for i in range(self.data.shape[-1]))
		rgb_sx = ndimage.sobel(rgb_gradient, axis=0, mode='constant')
		rgb_sy = ndimage.sobel(rgb_gradient, axis=1, mode='constant')

		h = (rgb_sx + rgb_sy)
		return h

	def iteration(self):
		"""
		Does one iteration of the method.

		"""
		laplace = self.get_laplace()
		laplace = laplace[:, :, 0] if (len(laplace.shape) == 3) else laplace

		self.results[1:-1, 1:-1] += (laplace[:, :] - self.h[1:-1, 1:-1]) * self.alpha
		self.results = self.neumann(self.results)

		self.data = self.results.clip(0, 1)

	#
	def fit(self, epochs):
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count
		"""
		for i in range(epochs):
			self.iteration()
		return self
