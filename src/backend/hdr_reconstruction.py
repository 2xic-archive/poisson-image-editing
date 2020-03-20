# TODO : http://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf
from engine import image_handler
from engine import poisson
from engine import boundary
import numpy as np
from PIL import Image


class hdr_reconstruction(image_handler.ImageHandler, poisson.poisson):
	"""
	This class describes a HDR image.

	This contains all the functions needed to perform HDR reconstruction on a image over multiple iterations

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
		self.alpha = 0.25
		
	def iteration(self):
		"""
		Does one iteration of the method.

		"""
		raise Exception("implement")
		return self.data

	def fit(self,epochs):
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
