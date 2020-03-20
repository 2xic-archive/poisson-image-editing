import image_handler
import poisson
import numpy as np
from inpaiting import *

class demosaic(image_handler.ImageHandler, poisson.poisson):
	def __init__(self, path, color=False):
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		self.alpha = 0.25
		self.inpait = inpait(None)

		self.simulate()
		self.inpait.data = self.mosaic

		self.results = np.zeros((self.mosaic.shape) + (3, ))
		self.results[:, :, 0] = self.mosaic
		self.results[:, :, 1] = self.mosaic
		self.results[:, :, 2] = self.mosaic

	def simulate(self):
		u = self.data
		self.mosaic = np.zeros(u.shape[:2])  # Alloker plass
		self.mosaic[ ::2, ::2] = u[ ::2, ::2, 0]  # R-kanal
		self.mosaic[1::2, ::2] = u[1::2, ::2, 1]  # G-kanal
		self.mosaic[ ::2, 1::2] = u[ ::2, 1::2, 1] # G-kanal
		self.mosaic[1::2, 1::2] = u[1::2, 1::2, 2] # B-kanal

		self.rgb_mosaic = np.zeros(self.mosaic.shape + (3, ))
		self.rgb_mosaic[:, :, 0] = self.mosaic[:, :]
		self.rgb_mosaic[:, :, 1] = self.mosaic[:, :]
		self.rgb_mosaic[:, :, 1] = self.mosaic[:, :]
		self.rgb_mosaic[:, :, 2] = self.mosaic[:, :]

		self.mask = np.ones(np.shape(self.mosaic) + (3, ))
		self.mask[ ::2, ::2, 0] = 0
		self.mask[1::2, ::2, 1] = 0
		self.mask[ ::2, 1::2, 1] = 0
		self.mask[1::2, 1::2, 2] = 0

		return self.mosaic


	def iteration(self):
		"""
		[TODO:summary]

		[TODO:description]
		"""
		self.inpait.alpha = 0.05
		self.inpait.set_demosaicing()
		for i in range(3):
			self.results[:, :, i] = self.inpait.fit(self.rgb_mosaic[:, :, i], self.results[:, :, i], self.mask[:, :, i])
		self.data = self.results

	def fit(self,epochs=1):
		"""
		[TODO:summary]

		[TODO:description]

		Parameters
		----------
		epochs : int
			The iteration count
		"""
		for i in range(epochs):
			self.iteration()
		return self