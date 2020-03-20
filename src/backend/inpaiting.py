import image_handler
import poisson
import numpy as np
from PIL import Image

class inpait(image_handler.ImageHandler, poisson.poisson):
	def __init__(self, path, color=False):
		if not path is None:
			image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)

		self.alpha = 0.25
		self.mask = None
		self.copy = None
		self.mode = "inpait"

	def set_demosaicing(self):
		self.mode = "demosaicing"

	def set_data(self, data):
		self.data = data

	def set_mask(self, mask):
		self.mask = mask

	def set_orignal(self, original):
		self.original_data = original

	def destroy_information(self, strength=2):
		noise = np.random.randint(0, 10, size=self.data.shape)
		mask = np.zeros(self.data.shape)

		mask[strength < noise ] = 1
		mask[noise < strength] = 0
#		print(mask)
		self.data *= mask
		self.mask = mask
		self.original_data = np.copy(self.data)
		return mask

	def iteration(self):
		laplace = self.get_laplance(self.data)
		self.data[1:-1, 1:-1] += self.alpha * laplace
		"""
		mask content
			original value = 1 
			infomation lost = 0 
		"""
		"""
			TODO: Figure out what is wrong here
		"""
		if(self.mode == "inpait"):
			self.data = (self.data * (1 - self.mask)) + (self.original_data * ( self.mask))
		else:
			self.data = (self.data * (self.mask)) + abs(self.original_data * (1 - self.mask))


	def fit(self, original=None, data=None, mask=None, epochs=1):
		if not mask is None:
			self.set_mask(mask)
		if not original is None:
			self.set_orignal(original)
		if not data is None:
			self.set_data(data)
		if(self.mask is None):
			raise Exception("You need to set a mask")
		
		for i in range(epochs):
			self.iteration()
		return self.data

