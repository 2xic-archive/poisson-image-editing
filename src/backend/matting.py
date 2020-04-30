from __future__ import annotations

from engine import image_handler
from engine import poisson
from engine import boundary

class matting(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
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
	def __init__(self, target_path="./files/test_images/target.png", source_path="./files/test_images/source_v2.png",
				 area=[[10, 65],
					[10, 65]],
				 padding=[50, 250],
				 color=True):
		"""
		self.bird = True

		if not self.bird:
			target_path = "./files/test_images/sky.jpg"
			source_path = "./files/test_images/moon.png"
		else:
			target_path = "./files/test_images/target.png"
			source_path = "./files/test_images/source_v2.png"
		"""
		image_handler.ImageHandler.__init__(self, target_path, color)
		boundary.Boundary.__init__(self)
		poisson.poisson.__init__(self)
		self.alpha = 0.1
		
		self.source = image_handler.ImageHandler(source_path, color)
		self.target = self.data.copy()

		# NOTE : If this is wide the effect will go badly (I tried without having this set and you
		# get a ugly border)
		# NOTE2 : I realized that it is because the photo contained a black border
		# TODO : Make it possible to set/define these values in GUI

		# OG SKY AND self.BIRD
		"""
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
		self.area = (
			(0, 0), 
			(0, 0)
		)
		"""
		self.area_full = area
		self.padding = padding# [0, 0]

	@property
	def area_full(self):
		return self._area

	@area_full.setter
	def area_full(self, mode):
		'setting'
		if len(mode) != 2:
			raise ValueError("You speify the area as a 2d tuple ((x0, x1), (y0, y1))")

		x0, x1 = mode[0]
		"""
		if x0 is None or x1 is None:
			raise ValueError("input should be a number")
		if not x0 < x1:
			raise ValueError("x0 should be less than x1")
		"""
		if x0 is None:
			x0 = 0
		if x1 is None:
			x1 = self.source.data.shape[1]

		if x0 < 0 or self.source.data.shape[1] < x1:
			raise ValueError("x range is ({}, {})".format(0, self.source.data.shape[1]))

		y0, y1 = mode[1]
#		if y0 is None or y1 is None:
#			raise ValueError("input should be a number")
		if y0 is None:
			y0 = 0
		if y1 is None:
			y1 = self.source.data.shape[0]

		if not y0 < y1:
			raise ValueError("y0 should be less than y1")
		if y0 < 0 or self.source.data.shape[0] < y1:
			raise ValueError("x range is ({}, {})".format(0, self.source.data.shape[0]))
		self._area = [(x0, x1), (y0, y1)]

	def preview_box(self, x, y, x1, y1):
		"""
		Preview the crop box
		"""
		self.area_full = ((x, x + self.source.data.shape[1]), (y, y + self.source.data.shape[0]))

		box = self.target.copy()
		x0, x1 = self.area_full[0][0], self.area_full[0][1]
		y0, y1 = self.area_full[1][0], self.area_full[1][1]
		box[y0:y1,
			x0:x1 :] = 255 
		return box

	def reset_full(self) -> None:
		"""
		Reset the image source and target
		"""
		self.source.reset()
		self.reset()

	def crop(self, x, with_padding=True):
		if with_padding:
			return x[self.area_full[1][0] + self.padding[1]:self.area_full[1][1]  + self.padding[1],
							  self.area_full[0][0] + self.padding[0]:self.area_full[0][1] + self.padding[0], :]
		return x[self.area_full[1][0]:self.area_full[1][1] ,
							  self.area_full[0][0]:self.area_full[0][1], :]

	def apply(self, data):
		for j in range(min(self.data.shape[-1], data.shape[-1])):
			self.data[self.area_full[1][0] + self.padding[1]:self.area_full[1][1] + self.padding[1], 
				self.area_full[0][0] + self.padding[0]:self.area_full[0][1] + self.padding[0], j] = data[:, :, j]

	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		"""
		#crop_area = lambda x: x[self.area_full[1][0] + self.padding[1]:self.area_full[1][1]  + self.padding[1],
		#					  self.area_full[0][0] + self.padding[0]:self.area_full[0][1] + self.padding[0], :]
		#crop_area_area = lambda x: x[self.area_full[1][0]:self.area_full[1][1] ,
		#					  self.area_full[0][0]:self.area_full[0][1], :]
		working_area = self.crop(self.data)
		working_area_source = self.crop(self.source.data, False)

	#	print(working_area_source.shape)
	#	print(working_area.shape)
	#	exit(0)
	#	import numpy as np
	#	from PIL import Image
	#	Image.fromarray((255 * working_area_source).astype(np.uint8)).show()
	#	Image.fromarray((255 * working_area).astype(np.uint8)).show()

		#if(self.bird):
		h = lambda i: self.get_laplace((working_area_source)[:, :, i]) #0.25 * crop_area(self.target)[:, :, i]) #self.target)#source.data[:, :, i]) #crop_area(self.source.data)[:, :, i])
	#	else:
	#		h = lambda i: self.get_laplace(working_area_source[:, :, i]) #0.25 * crop_area(self.target)[:, :, i]) #self.target)#source.data[:, :, i]) #crop_area(self.source.data)[:, :, i])
		operator = lambda i=None: self.get_laplace(working_area[:, :, i])#crop_area(self.target)[:, :, i]) 
		working_area = self.solve(working_area,operator, h, apply_boundary=False) #* self.alpha

		import numpy as np
		from PIL import Image
	#	x = np.zeros((working_area_source.shape + (3, )))
	#	print(working_area_source.shape)
	#	Image.fromarray((working_area_source * 255).astype(np.uint8)).convert('RGB').show()
	#	Image.fromarray((working_area * 255).astype(np.uint8)).convert('RGB').show()
	#	print(np.all(working_area == working_area_source))
		#print(working_area)
		#self.data[self.area_full[1][0] + self.padding[1]:self.area_full[1][1] + self.padding[1], 
		#self.area_full[0][0] + self.padding[0]:self.area_full[0][1] + self.padding[0]] =
		self.apply(working_area.clip(0, 1))

		"""
		Huh, so setting it as abs seems to solve the problem when working with implicit....
		I will ask Ivar if this is supposed to happen
		it could also mean that there is a sign problem
		"""
		"""
		if(self.bird):
			working_area[:, :, 0] = abs(self.get_laplace_implicit(working_area[:, :, 0]) - self.get_laplace_implicit(crop_area(self.source.data)[:, :, 0]))
			working_area[:, :, 1] = abs(self.get_laplace_implicit(working_area[:, :, 1]) - self.get_laplace_implicit(crop_area(self.source.data)[:, :, 1]))
			working_area[:, :, 2] = abs(self.get_laplace_implicit(working_area[:, :, 2]) - self.get_laplace_implicit(crop_area(self.source.data)[:, :, 2]))
		else:
			working_area[:, :, 0] = abs(self.get_laplace_implicit(working_area[:, :, 0]) - self.get_laplace_implicit((self.source.data)[:, :, 0]))
			working_area[:, :, 1] = abs(self.get_laplace_implicit(working_area[:, :, 1]) - self.get_laplace_implicit((self.source.data)[:, :, 1]))
			working_area[:, :, 2] = abs(self.get_laplace_implicit(working_area[:, :, 2]) - self.get_laplace_implicit((self.source.data)[:, :, 2]))
		"""
		# TODO : make this "nice"
		#print(working_area.max())
		#print(working_area.min())


	def bad_fit(self):
#		print(self.area_full)
		working_area_source = self.crop(self.source.data, with_padding=False)
		from PIL import Image
#		print(working_area_source)
#		Image.fromarray(working_area_source).convert('RGB').show()
		self.apply(working_area_source)
#		print(working_area_source.shape)

		#	= working_area_source.clip(0, 1)

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
