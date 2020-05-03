from __future__ import annotations
from engine import hdr_image_handler
from engine import image_handler

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
	def __init__(self, images=None, color=True):
		if images is None:
			images = [
				image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00064.png'),
				image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00128.png'),
				image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00256.png'),
				image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00512.png')
			]
		self.handler = hdr_image_handler.hdr_handler(images=images)
		path = self.handler.images[0].path
		image_handler.ImageHandler.__init__(self, path, color)

	def update_images(self, images):
		"""
			update the class with another set of images
		"""
		self.handler = hdr_image_handler.hdr_handler(images=
			[image_handler.ImageHandler(i) for i in images]
		)

	def fit(self,epochs=1) -> hdr_reconstruction:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count

		Returns
		-------
		hdr_reconstruction
			returns self
		"""
		radiance = self.handler.get_radiance()
		self.radiance_log = self.handler.get_radiance_log(radiance)
		self.data = self.handler.normalize(self.radiance_log)
		return self
