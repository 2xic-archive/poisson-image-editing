import loader
import numpy as np
from PIL import Image

class inpait(loader.ImageLoader):
	def __init__(self, path, color=False):
		loader.ImageLoader.__init__(self, path, color)

		self.alpha = 0.25
		self.mask = None
#		self.mask = self.destroy_information()

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

	def eksplisitt(self):
		laplace = self.get_laplance(self.original_data)
		self.original_data[1:-1, 1:-1] += self.alpha * laplace
		"""
		mask content
			original value = 1 
			infomation lost = 0 
		"""
		self.data = (self.data * (self.mask)) + abs(self.original_data * (1 - self.mask))

	def fit(self, epochs=1):
		if(self.mask is None):
			# TODO: In the future you should be able to set a mask manually. 
			raise Exception("You need to destroy infomation in the image before you run this function")
		for i in range(epochs):
			self.eksplisitt()