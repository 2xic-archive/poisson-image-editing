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
#		self.mask = self.destroy_information()

	def set_data(self, data):
		self.data = data

	def set_mask(self, mask):
		self.mask = mask

	def set_orignal(self, original):
		self.original_data = original

	def destroy_information(self, strength=2):
		self.original_data = np.copy(self.data)
		noise = np.random.randint(0, 10, size=self.data.shape)
		mask = np.zeros(self.data.shape)

		mask[strength < noise ] = 1
		mask[noise < strength] = 0
#		print(mask)
		self.data *= mask
		self.mask = mask
		return mask

	def iteration(self):
		laplace = self.get_laplance(self.original_data)
		self.original_data[1:-1, 1:-1] += self.alpha * laplace
		"""
		mask content
			original value = 1 
			infomation lost = 0 
		"""
#		print(self.data is None)
#		print(self.mask is None)
#		print(self.original_data is None)		
		self.data = (self.data * (self.mask)) + abs(self.original_data * (1 - self.mask))

	def fit(self, epochs=1, mask=None):
		if not mask is None:
			self.mask = mask
		if(self.mask is None):
			raise Exception("You need to set a mask")
		for i in range(epochs):
			self.iteration()
		return self.data

