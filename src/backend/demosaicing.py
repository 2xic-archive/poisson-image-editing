from __future__ import annotations
from engine import image_handler
from engine import poisson
import numpy as np
from backend import inpaiting
from engine import poisson, boundary
from nptyping import Array

class Demosaic(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a demosaic image.

	This contains all the functions needed to perform demosaic on a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""

	def __init__(self, path: str, color: bool = True):
		self.inpaint = inpaiting.inpaint(None)
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		boundary.Boundary.__init__(self)
		self.simulated = False

	@property
	def alpha(self):
		"""
		Get the alpha value for inpait

		Returns
		-------
		float
			alpha value
		"""
		return self.inpaint.alpha

	@alpha.setter
	def alpha(self, alpha):
		"""
		Sets the alpha value for inpait

		Parameters
		----------
		alpha : float
			The alpha value to use
		"""
		self.inpaint.alpha = alpha

	@property
	def mode_poisson(self):
		"""
		Get the mode for the poission backend

		Returns
		----------
		int
			the mode id
		"""
		return self.inpaint.mode_poisson

	@mode_poisson.setter
	def mode_poisson(self, mode_poisson):
		"""
		Set the mode for the poission backend
		
		Parameters
		----------
		mode_poisson : int
			The mode value to use
		"""
		self.inpaint.mode_poisson = mode_poisson

	@property
	def mode_boundary(self):
		"""
		Get the mode for the boundary

		Returns
		----------
		int
			the mode id
		"""
		return self.inpaint.mode_boundary

	@mode_boundary.setter
	def mode_boundary(self, mode_boundary):
		"""
		Set the mode for the boundary

		Returns
		----------
		int
			the mode id
		"""
		self.inpaint.mode_boundary = mode_boundary

	def reset(self):
		"""
		Reset the method

		sets the image to the orignal image. Removes the mosaic. 
		"""
		self.data = self.data_copy.copy()
		self.simulated = False
		self.get_mosaic()
		self.inpaint.data = self.mosaic        

	def get_mosaic(self):
		"""
		Simulates the mosaic
		"""
		self.mosaic = np.zeros(self.data.shape[:2])
		self.mosaic[::2, ::2] = self.data[::2, ::2, 0]
		self.mosaic[1::2, ::2] = self.data[1::2, ::2, 1]
		self.mosaic[::2, 1::2] = self.data[::2, 1::2, 1]
		self.mosaic[1::2, 1::2] = self.data[1::2, 1::2, 2]

	def simulate(self):
		"""
		Simualtes a image into a state where we can preform demosaic

		Returns
		-------
		array
			the simulated mosaic image
		"""
		self.get_mosaic()
		self.rgb_mosaic = np.asarray([
			self.mosaic,
			self.mosaic,
			self.mosaic
		]).reshape(self.mosaic.shape + (3, ))

		self.mask = np.zeros(np.shape(self.mosaic) + (3,))
		self.mask[::2, ::2, 0] = 1
		self.mask[1::2, ::2, 1] = 1
		self.mask[::2, 1::2, 1] = 1
		self.mask[1::2, 1::2, 2] = 1

		#	set the inpait data
		self.inpaint.data = self.mosaic.copy()
		self.inpaint.data_copy = self.mosaic.copy()

		self.results = np.zeros(self.mosaic.shape + (3,))
		self.results[:, :, 0] = self.mosaic
		self.results[:, :, 1] = self.mosaic
		self.results[:, :, 2] = self.mosaic

		self.simulated = True
		self.data = self.mosaic

		return self.mosaic

	def iteration(self) -> Array:
		"""
		Does one iteration of the method.

		Returns
		-------
		array
			the new image array
		"""
		self.verify_integrity()

		for i in range(3):
			self.results[:, :, i] = self.inpaint.fit(self.rgb_mosaic[:, :, i], self.results[:, :, i], self.mask[:, :, i])
		self.data = self.results
		self.data = self.data.clip(0, 1)		
		return self.data

	def fit(self, epochs: int = 1) -> Demosaic:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count

		Returns
		-------
		Demosaic
			returns self
		"""
		if not self.simulated:
			raise Exception("You have to simulate the mosaic first")

		for i in range(epochs):
			self.iteration()
		return self
