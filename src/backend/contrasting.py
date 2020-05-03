from engine import poisson, boundary
from engine import image_handler
import numpy as np


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

		self.alpha = 0.2
		self.k = 5
		if len(self.data.shape) == 2:
			self.h = self.k * self.get_laplace(np.copy(self.data))
		else:
			self.h = self.k * (np.asarray([self.get_laplace(np.copy(self.data[:, :, i]))
				for i in range(self.data.shape[-1])]))
			#print(self.h.shape)

	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		Returns
		-------
		array
			the new image array
		"""		
		self.verify_integrity()

		def operator(i):
			if i is None:
				return 0.2 * self.get_laplace(self.data, alpha=False) 
			else:
				return 0.2 * self.get_laplace(self.data[:, :, i], alpha=False)

		def h(i=None):
			if len(self.h.shape) == 3:
				return self.h[i, :, :]
			else:
				return self.h
		
		self.data = self.solve(self.data, operator, h)
		return self.data

	def fit(self, epochs=1):
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
