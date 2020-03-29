from __future__ import annotations
# TODO : http://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf
from engine import image_handler
from engine import poisson
from engine import boundary
import numpy as np
from PIL import Image
from nptyping import Array
from engine import hdr_image_handler

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
	def __init__(self, color=True):
		self.handler = hdr_image_handler.hdr_handler()
		path = self.handler.images[0].path

		image_handler.ImageHandler.__init__(self, path, color)

#		self.show()
#		print(np.max(self.data))
#		print(np.min(self.data))
#		exit(0)

		poisson.poisson.__init__(self)

#		x = hdr_image_handler.hdr_handler()
		self.alpha = 0.25
		
	def iteration(self) -> Array:
		"""
		Does one iteration of the method.

		"""
		raise Exception("implement")
		return self.data

	def fit(self,epochs) -> hdr_reconstruction:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count
		"""
		radiance = self.handler.get_radiance()
		self.radiance_log = self.handler.get_radiance_log(radiance)
		self.data = self.handler.normalize(self.radiance_log)
#		for i in range(epochs):
#			self.iteration()
		return self
