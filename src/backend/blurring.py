from engine import poisson, boundary, image_handler
import numpy as np
from nptyping import Array

class blur(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a blured image.

	This contains all the functions needed to blur a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""
	def __init__(self, path, color=False):
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		boundary.Boundary.__init__(self)
		if not path is None:
			self.set_boundary(self.NEUMANN)
		self.alpha: float = 0.25
		self.lambda_size: float = 0.1

	def set_lambda_size(self, lambda_size) -> None:
		"""
		Sets the lambda fro data attachment

		Parameters
		----------
		lambda_size : float
			The lambda parameter
		"""
		self.lambda_size = lambda_size
		
	def iteration(self) -> Array:
		"""
		Does one iteration of the method.

		Returns
		-------
		array
			numpy array with the new image after the iteration
		"""
		assert 0 <= self.lambda_size <= 1, "lamda is out of scope [0, 1]"
		self.verify_integrity()
		self.data = self.solve(self.data, self.opeartor, self.h)
		return self.data

	def opeartor(self, i=None):
		"""
		Solves the "u" part of the poisson equation

		Returns
		-------
		array
			the u value
		"""
		if i is None:
			return self.get_laplace(self.data, alpha=True) 
		else:
			return self.get_laplace(self.data[:, :, i], alpha=True)		

	def h(self, i=None):
		"""
		Solves the "h" part of the poisson equation

		Returns
		-------
		array
			the h value
		"""
		if i is None:
			return self.common_shape(self.lambda_size * (self.data - self.data_copy))
		else:
			return self.common_shape(self.lambda_size * (self.data[:, :, i] - self.data_copy[:, :, i]))
		
	def fit(self, epochs):# -> blur:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count

		Returns
		-------
		blur
			returns self
		"""
		for i in range(epochs):
			self.iteration()
		return self


