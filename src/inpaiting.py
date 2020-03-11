import loader
import numpy as np
from PIL import Image

class inpait(loader.ImageLoader):
	def __init__(self, path, color=False):
		loader.ImageLoader.__init__(self, path, color)

		self.alpha = 0.25
		self.mask = self.destroy_information()
		self.original_data = np.copy(self.data)

	def destroy_information(self):
		noise = np.random.randint(0, 10, size=self.data.shape)
		mask = np.zeros(self.data.shape)

		mask[2 < noise ] = 1
		mask[noise < 2] = 0
		print(mask)
		self.data *= mask
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
		for i in range(epochs):
			self.eksplisitt()