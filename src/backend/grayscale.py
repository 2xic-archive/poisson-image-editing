from __future__ import annotations
from engine import image_handler
import numpy as np
from engine import poisson
from engine import boundary
from nptyping import Array

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
		assert color == True, "we can only grayscale images that have color"

		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		boundary.Boundary.__init__(self)

		self.alpha = 0.25

		self.avg = self.data.copy().mean(axis=2)
		self.results = np.zeros((self.data.shape[:2]))

	def reset(self):
		"""
		Reset the method
		"""
		self.data = self.data_copy.copy()

	def h_func(self) -> Array:
		"""
			The h variable of the poisson eq
		"""
		# why does this not work ? Find out !
		#g_length = np.sum(self.get_gradient_norm(self.data_copy[:, :, i]) for i in range(3))#/ np.sqrt(3)
		image_r_x, image_r_y = self.get_gradient(self.data_copy[:, :, 0])
		image_g_x, image_g_y = self.get_gradient(self.data_copy[:, :, 1])
		image_b_x, image_b_y = self.get_gradient(self.data_copy[:, :, 2])
		g_length = np.sqrt(
			(image_r_x**2 + image_r_y**2 +
			 image_g_x**2 + image_g_y**2 +
			 image_b_x**2 + image_b_y**2) / 3
		)

		rgb_sum = np.sum(self.data_copy[:, :, i] for i in range(self.data_copy.shape[-1]))
		rgb_sx, rgb_sy = self.get_gradient(rgb_sum)

		length = np.sqrt(rgb_sx ** 2 + rgb_sy ** 2)
		length[length == 0] = np.finfo(float).eps

		rgb_sx /= length
		rgb_sy /= length

		h_prime_x, h_prime_y = rgb_sx * g_length , rgb_sy * g_length
		
		h_sx, _ = self.get_gradient(h_prime_x)
		_, h_sy = self.get_gradient(h_prime_y)

		return (h_sx + h_sy)

	def iteration(self) -> None: 
		"""
		Does one iteration of the method.

		Returns
		-------
		array
			the new image array
		"""

		"""
			Reset the dimension on first round
		"""
		if len(np.shape(self.data)) == 3:
			self.data = self.data.mean(axis=2)
			self.h = self.h_func()
		
		self.verify_integrity()
		
		operator = lambda : self.get_laplace(self.data, alpha=False)
		h = lambda x: self.h[1:-1, 1:-1]
	
		self.data[1:-1, 1:-1] = self.data[1:-1, 1:-1] + 0.2 * (operator()- h(None))

		self.data = self.neumann(self.data)
		self.data = self.data.clip(0, 1)

		return self.data

	def fit(self, epochs) -> grayscale:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count

		Returns
		-------
		grayscale
			returns self
		"""
		for _ in range(epochs):
			self.iteration()
		return self
