import image_handler
import poisson
import numpy as np

class matting(image_handler.ImageHandler, poisson.poisson):
	def __init__(self, path, color=True):
		path = "../test_images/target.png"
		source = "../test_images/source.png"

		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		self.alpha = 0.2

		# the bird
		self.source = image_handler.ImageHandler(source, color)
		self.target = self.data.copy()

		# NOTE : If this is wide the effect will go badly (I tried without having this set and you 
		# get a ugly border)
		# TODO : Make it possible to set/define these values in GUI
		self.area = (
			(200, 50),
			(250, 130),
		)
		print(self.area)

	def get_area(self):


	def iteration(self):
		"""
		[TODO:summary]

		[TODO:description]
		"""
		crop_area = lambda x: x[self.area[0][0]:self.area[1][0], 
								self.area[0][1]:self.area[1][1]]

		target_laplace = self.get_laplance(crop_area(self.target))
		source_laplace = self.get_laplance(crop_area(self.source.data))
		working_area = crop_area(self.data)
		working_area[1:-1, 1:-1] += (target_laplace - source_laplace) * self.alpha

		# TODO : make this "nice"
		self.data[self.area[0][0]:self.area[1][0], 
			self.area[0][1]:self.area[1][1]] = working_area.clip(0, 1)

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