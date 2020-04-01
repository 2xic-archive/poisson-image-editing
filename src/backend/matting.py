from __future__ import annotations

from engine import image_handler
from engine import poisson


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
		self.bird = False

		if not self.bird:
			target_path = "./files/test_images/sky.jpg"
			source_path = "./files/test_images/moon.png"
		else:
			target_path = "./files/test_images/target.png"
			source_path = "./files/test_images/source.png"

		image_handler.ImageHandler.__init__(self, target_path, color)
		poisson.poisson.__init__(self)
		self.alpha = 0.1

		# currently no good support for non 2d array
		#self.mode_poisson = self.EXPLICIT
		#
		#
		
		# the self.bird
		self.source = image_handler.ImageHandler(source_path, color)
		self.target = self.data.copy()

#		print((self.get_laplace_explicit(self.source.data[:, :, 0])- self.get_laplace_implicit(self.source.data[:, :, 0])[1:-1, 1:-1]).sum())
#		print((self.get_laplace_explicit(self.source.data[:, :, 0])- self.get_laplace_implicit(self.source.data[:, :, 0])[1:-1, 1:-1]).sum())
#		exit(0)

		# NOTE : If this is wide the effect will go badly (I tried without having this set and you
		# get a ugly border)
		# NOTE2 : I realized that it is because the photo contained a black border
		# TODO : Make it possible to set/define these values in GUI

		# OG SKY AND self.BIRD
		if self.bird:
			self.area = (
				(200, 80),
				(250, 130),
			)
		else:
			self.area = (
				(200, 150),
				(200 + self.source.data.shape[0], 150 + self.source.data.shape[1]),
			)		
	#	self.preview_box()

	def preview_box(self):
		"""
		Preview the crop box
		"""
		self.target[self.area[0][0]:self.area[1][0],
							  self.area[0][1]:self.area[1][1], :] = self.source.data[:, :, :]
		self.data = self.target
		self.show()
		exit(0)


	def reset_full(self) -> None:
		"""
		Reset the image source and target
		"""
		self.source.reset()
		self.reset()

	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		"""
		crop_area = lambda x: x[self.area[0][0]:self.area[1][0],
							  self.area[0][1]:self.area[1][1], :]
		working_area = crop_area(self.data)

		if(self.bird):
			h = lambda i: self.get_laplace(crop_area(self.source.data)[:, :, i]) #0.25 * crop_area(self.target)[:, :, i]) #self.target)#source.data[:, :, i]) #crop_area(self.source.data)[:, :, i])
		else:
			h = lambda i: self.get_laplace(self.source.data[:, :, i]) #0.25 * crop_area(self.target)[:, :, i]) #self.target)#source.data[:, :, i]) #crop_area(self.source.data)[:, :, i])
#		operator = lambda i=None: self.get_laplace(crop_area(self.target)[:, :, i]) 
#		working_area = abs(self.solve(working_area,operator, h)) #* self.alpha
			
		"""
		Huh, so setting it as abs seems to solve the problem when working with implicit....
		I will ask Ivar if this is supposed to happen
		it could also mean that there is a sign problem
		"""
		if(self.bird):
			working_area[:, :, 0] = abs(self.get_laplace_implicit(working_area[:, :, 0]) - self.get_laplace_implicit(crop_area(self.source.data)[:, :, 0]))
			working_area[:, :, 1] = abs(self.get_laplace_implicit(working_area[:, :, 1]) - self.get_laplace_implicit(crop_area(self.source.data)[:, :, 1]))
			working_area[:, :, 2] = abs(self.get_laplace_implicit(working_area[:, :, 2]) - self.get_laplace_implicit(crop_area(self.source.data)[:, :, 2]))
		else:
			working_area[:, :, 0] = abs(self.get_laplace_implicit(working_area[:, :, 0]) - self.get_laplace_implicit((self.source.data)[:, :, 0]))
			working_area[:, :, 1] = abs(self.get_laplace_implicit(working_area[:, :, 1]) - self.get_laplace_implicit((self.source.data)[:, :, 1]))
			working_area[:, :, 2] = abs(self.get_laplace_implicit(working_area[:, :, 2]) - self.get_laplace_implicit((self.source.data)[:, :, 2]))

		# TODO : make this "nice"
		print(working_area.max())
		print(working_area.min())
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
	#	self.show()
		return self
