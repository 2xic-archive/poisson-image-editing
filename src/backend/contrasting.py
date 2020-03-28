from engine import poisson
from engine import image_handler
import numpy as np


class Contrast(image_handler.ImageHandler, poisson.poisson):
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
		self.alpha = 0.1
		self.k = 1
		self.u0 = np.copy(self.data)

	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		"""
	#	laplace = self.get_laplace()
		#    TODO: check if this is correct. 
#		self.data = self.solve(self.u0, 
#			h=(lambda x:(self.k * self.get_laplace() * self.alpha)),
#			results=self.data)
#		h = lambda x: (self.lambda_size * (self.data - self.data_copy))
		
		operator = lambda : self.common_shape(self.u0)
		h = lambda x: (self.k  * self.get_laplace(self.data))
		
		self.data = self.solve(self.data, operator, h) 
		self.data = self.data.clip(0, 1)
	#	self.data = self.neumann(self.data)


#		self.data[1:-1, 1:-1] += (self.u0[1:-1, 1:-1] - (self.k * laplace)) * self.alpha
		# ((laplace) - (self.k * self.u0[1:-1, 1:-1])) * self.alpha <- guess i had it backwards?
#		self.data = self.data.clip(0, 1)


		"""
		TODO : Implement Neumann
		"""

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
