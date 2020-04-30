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
		self.h = self.k * self.get_laplace(np.copy(self.data))

	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		"""		
		self.verify_integrity()

		operator = lambda : self.get_laplace(self.data)
		h = lambda x: self.h
		
		self.data = self.solve(self.data, operator, h)
		
	def fit(self, epochs=1):
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
