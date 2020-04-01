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

	def h(self) -> Array:
		"""
			The h variable of the poisson eq
		"""
		g = np.sum(self.get_gradient_norm(self.data_copy)[:, :, i] for i in range(3))/ np.sqrt(3)

		rgb_gradient = np.sum(self.data_copy[:, :, i] for i in range(self.data_copy.shape[-1]))
		rgb_sx, rgb_sy = self.get_gradient(rgb_gradient)

		h = rgb_sx + rgb_sy
		return h * g

	def iteration(self) -> None: 
		"""
		Does one iteration of the method.

		"""

		"""
			Reset the dimension on first round
		"""
		if len(np.shape(self.data)) == 3:
			self.data = self.data.mean(axis=2)

		self.verify_integrity()
		operator = lambda : self.get_laplace(self.data) 
		h = lambda x: self.common_shape(self.h())
		
		self.data = self.solve(self.data, operator, h) 
		self.data = self.neumann(self.data)
		self.data = self.data.clip(0, 1)


	def fit(self, epochs) -> grayscale:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count
		"""
		for _ in range(epochs):
			self.iteration()
		return self
