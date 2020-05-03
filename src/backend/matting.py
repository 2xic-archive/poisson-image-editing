from __future__ import annotations

from engine import image_handler
from engine import poisson
from engine import boundary
from PIL import Image
		
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

		image_handler.ImageHandler.__init__(self, target_path, color)
		boundary.Boundary.__init__(self)
		poisson.poisson.__init__(self)
		self.alpha = 0.1
		
		self.source = image_handler.ImageHandler(source_path, color)
		self.target = self.data.copy()

		self.area_full = area
		self.padding = padding

	@property
	def area_full(self):
		"""
		Return the working area
		"""
		return self._area

	@area_full.setter
	def area_full(self, mode):
		"""
		Setter for the working area

		This is a setter that makes sure that the data that is set is valid.
		"""
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

		Returns
		-------
		array
			the cropbox
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
		"""
		Crops the image


		Returns
		-------
		array
			the new cropped image array
		"""
		if with_padding:
			return x[self.area_full[1][0] + self.padding[1]:self.area_full[1][1]  + self.padding[1],
							  self.area_full[0][0] + self.padding[0]:self.area_full[0][1] + self.padding[0], :]
		return x[self.area_full[1][0]:self.area_full[1][1] ,
							  self.area_full[0][0]:self.area_full[0][1], :]

	def apply(self, data):
		"""
		Apply the data to the image

		Sets the new data based on the padding and area size
		"""
		for j in range(min(self.data.shape[-1], data.shape[-1])):
			self.data[self.area_full[1][0] + self.padding[1]:self.area_full[1][1] + self.padding[1], 
				self.area_full[0][0] + self.padding[0]:self.area_full[0][1] + self.padding[0], j] = data[:, :, j]

	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		Returns
		-------
		array
			the new image array
		"""
		working_area = self.crop(self.data)
		working_area_source = self.crop(self.source.data, False)
		
		h = lambda i: self.get_laplace((working_area_source)[:, :, i])
		operator = lambda i=None: self.get_laplace(working_area[:, :, i])
		working_area = self.solve(working_area,operator, h, apply_boundary=False)

		self.apply(working_area.clip(0, 1))

		return self.data

	def bad_fit(self):
		"""
		Will directly paste the source image onto the target image
		"""
		working_area_source = self.crop(self.source.data, with_padding=False)
		self.apply(working_area_source)

	def fit(self, epochs=1) -> matting:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count

		Returns
		-------
		matting
			returns self
		"""
		for i in range(epochs):
			self.iteration()
		return self
