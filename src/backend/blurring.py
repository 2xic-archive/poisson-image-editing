from engine import poisson, boundary, image_handler
#engine.image_handler import ImageHandler
#import poisson
#import boundary
import numpy as np
from PIL import Image


#   TODO: Add support for "data attachment"

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
		self.alpha: float = 0.25
		self.lambda_size: float = 0

	def set_lambda_size(self, lambda_size):
		"""
		Sets the lambda fro data attachment

		Parameters
		----------
		lambda_size : float
			The lambda parameter
		"""
		self.lambda_size = "test"#lambda_size
		
	def iteration(self):
		"""
		Does one iteration of the method.

		"""
		laplace = self.get_laplace()
		print(self.lambda_size)
		old = self.data.copy()

		# TODO : Seems like data attachment works, but it still "flickers" after some iterations, figure out why 
		self.data[1:-1, 1:-1] += (self.alpha * laplace) - (self.lambda_size * (self.data[1:-1, 1:-1] - self.data_copy[1:-1, 1:-1]))
		self.data = self.data.clip(0, 1)
		self.data = self.neumann(self.data)
		self.data = self.data.clip(0, 1)
		print((old - self.data).sum())
		return self.data

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
