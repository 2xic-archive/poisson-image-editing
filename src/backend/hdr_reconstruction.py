from __future__ import annotations
from engine import hdr_image_handler
from engine import image_handler

# TODO : http://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf

class hdr_reconstruction(image_handler.ImageHandler):
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
		return self
