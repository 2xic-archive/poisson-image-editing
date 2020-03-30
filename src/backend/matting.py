from __future__ import annotations

from engine import image_handler
from engine import poisson
from gui.general import get_path


class matting(image_handler.ImageHandler, poisson.poisson):
	"""
	This class describes a matting image.

	This contains all the functions needed to merge a image over another image over multiple iterations

	Parameters
	----------
	target_path : str
		path to the target image
	source_path : str
		path to a souce image to add on the target
	color : bool
		if the image should be shown with colors
	"""
	def __init__(self, target_path="./files/test_images/target.png", source_path="./files/test_images/source.png",
				 color=True):
	#	target_path = "./files/test_images/target.jpg"
	#	source_path = "./files/test_images/ntnu.jpg"

		image_handler.ImageHandler.__init__(self, target_path, color)
		poisson.poisson.__init__(self)
		self.alpha = 0.2

		# currently no good support for non 2d array
		#self.mode_poisson = self.EXPLICIT
		#
		#
		
		# the bird
		self.source = image_handler.ImageHandler(source_path, color)
		self.target = self.data.copy()

#		print((self.get_laplace_explicit(self.source.data[:, :, 0])- self.get_laplace_implicit(self.source.data[:, :, 0])[1:-1, 1:-1]).sum())
#		print((self.get_laplace_explicit(self.source.data[:, :, 0])- self.get_laplace_implicit(self.source.data[:, :, 0])[1:-1, 1:-1]).sum())
#		exit(0)

		# NOTE : If this is wide the effect will go badly (I tried without having this set and you
		# get a ugly border)
		# NOTE2 : I realized that it is because the photo contained a black border
		# TODO : Make it possible to set/define these values in GUI
		self.area = (
			(200, 80),
			(250, 130),
		)
		print(self.area)

	def reset_full(self) -> None:
		self.source.reset()# = image_handler.ImageHandler(self.source_path, color)
		self.reset()
#		self.target = self.data.copy()


	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		"""
		crop_area = lambda x: x[self.area[0][0]:self.area[1][0],
							  self.area[0][1]:self.area[1][1], :]
		working_area = crop_area(self.data)

		"""
		TODO : Problem, since the image has extra dimension the implicit method is not happy
				I think the way to solve it is to iterate over each channel
		"""
		h = lambda i: self.get_laplace(crop_area(self.source.data)[:, :, i])
		operator = lambda i=None: self.get_laplace(crop_area(self.target)[:, :, i]) 
		working_area = self.solve(working_area,operator, h)


		# TODO : make this "nice"
		self.data[self.area[0][0]:self.area[1][0], self.area[0][1]:self.area[1][1]] = working_area.clip(0, 1)

	def fit(self, epochs=1) -> matting:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count
		"""
		for i in range(epochs):
			self.iteration()
		return self
