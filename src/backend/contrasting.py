from engine import poisson, boundary
from engine import image_handler
import numpy as np
from nptyping import Array

class Contrast(image_handler.ImageHandler, poisson.poisson,boundary.Boundary):
	"""
	This class describes a contrast image.

	This contains all the functions needed to improve the contrast of a image over multiple iterations

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
		boundary.Boundary.__init__(self, self.data.copy())

		self.mode_boundary = "neumann"
		self.alpha = 0.2
		self.k = 2
		if len(self.data.shape) == 2:
			self.h_arr = self.k * self.get_laplace(np.copy(self.data), alpha=True)
		else:
			self.h_arr = self.k * (np.asarray([self.get_laplace(np.copy(self.data[:, :, i]))
				for i in range(self.data.shape[-1])]))

	def iteration(self) -> Array:
		"""
		Does one iteration of the method.

		Returns
		-------
		array
			the new image array
		"""		
		self.verify_integrity()

		self.data = self.solve(self.data, self.operator, self.h)
		#self.data = self.neumann(self.data)
		return self.data

	def operator(self, i=None):
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
		if len(self.h_arr.shape) == 3:
			return self.h_arr[i, :, :]
		else:
			return self.h_arr

	def fit(self, epochs=1):# -> Contrast:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count

		Returns
		-------
		Contrast
			returns self
		"""
		for i in range(epochs):
			self.iteration()
		return self
