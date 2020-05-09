import numpy as np
from PIL import Image
from nptyping import Array


class ImageHandler:
	"""
	This class describes the functions for making it easy to interact with a image
	"""
	def __init__(self, path: str = None, color: bool = True):
		"""
		init the class

		Parameters
		----------
		path : str
			the location of the image, can be none (if you want to set 
			the data manually)
		color : bool
			if you want to have a color image and want to make it to grayscale
		"""
		if not path is None:
			self.color = color
			self.change_photo(path)

	def change_photo(self, path):
		"""
		Change out the photo 

		Changes out the photo, but keeps the same size as the old photo.

		Parameters
		----------
		path : str
			the location of the image, can be none (if you want to set 
			the data manually)

		Returns
		-------
		list
			returns the change in size
		"""
		self.path = path
		image = Image.open(path)
		image.load()

		movment = [0, 0]
		if hasattr(self, 'data'):
			old_size = self.data.shape[:2]
			image.thumbnail(old_size, Image.ANTIALIAS)
			new_size = image.size
			movment[0] = abs(old_size[0] - new_size[0]) / 2

		self.process(image)
		return movment

	def verify_integrity(self):
		"""
		Make sure that the image is in scope
		"""
		assert 0 <= self.data.max() <= 1, "data is out of scope [0, 1]"
		assert 0 <= self.data.min() <= 1, "data is out of scope [0, 1]"

	def change_color_state(self):
		"""
		Goes from color to gray, or gray to color

		Assuming the original image was a color image
		"""
		assert len(self.original_data.shape ) == 3, "the original image was not with color"
		self.color =  not self.color
		self.data = self.original_data.copy()
		self.convert_image()

	def resize(self, scale=8):
		"""
		Resize the image
		
		Parameters
		----------
		scale : int 
			Set the scale you want to resize
		"""
		im = Image.open(self.path)
		width, height = im.size
		im = im.resize((width//scale, height//scale))
		self.process(im)

	def convert_image(self):
		"""
		Converts image to scale [0, 1] 

		Will also convert to grayscale if specified 
		"""
		self.original_data = self.data.copy()
		if not self.color and not len(self.data.shape) == 2:
			self.data = self.convert_grayscale()
		else:
			self.data = self.normalize()
		self.data_copy = self.data.copy()

	def process(self, image):
		"""
		Processes the given image.
		
		Makes the image from a PIL image to numpy array and normalize it. 
		Will aslo convert the image to grayscale if specified.

		Parameters
		----------
		image : PIL.Image
			the input iamge
		"""
		self.data = np.asarray(image, dtype="float64").copy()
		self.convert_image()

	def set_data(self, data: Array):
		"""
		Set the data (image)

		Parameters
		----------
		data : ndarray
			the image data 
		"""
		self.data = data
		self.data_copy = self.data.copy()

	def reset(self):
		"""
		Reset the data (set's the image to the original)

		Using the data copy
		"""
		self.data = self.data_copy.copy()

	def get_gradient_norm(self, data: Array = None) -> Array[float]:
		"""
		Get the image gradient norm

		Parameters
		----------
		data : ndarray
			the image data
		
		Returns
		-------
		ndarray
			the gradient norm of the data
		"""
		if data is None:
			data = self.data
		g_x, g_y = self.get_gradient(data)
		return np.sqrt(g_x ** 2 + g_y ** 2)

	def get_gradient(self, data: Array) -> Array:
		"""
		Get the image gradient

		Parameters
		----------
		data : ndarray
			the image data

		Returns
		-------
		ndarray
			the gradient for x and y
		"""
		if data is None:
			data = self.data
		g_x, g_y = np.gradient(data, axis=[0, 1])
		return g_x, g_y

	def convert_grayscale(self, data=None):
		"""
		Makes the color image a grayscale image

		Asummes a color image

		Parameters
		----------
		data : Array
			the color image

		Returns
		-------
		ndarray
			the grayscale image
		"""
		if data is None:
			data = self.data
		assert len(data.shape) == 3, "Input was not a color image"
		data = np.sum(data.astype(float), 2) / (3 * 255)
		data = data.clip(0, 1)
		return data

	def normalize(self, data=None):
		"""
		Normalize the image [0, 1]

		Parameters
		----------
		data : Array
			the color image

		Returns
		-------
		ndarray
			the grayscale image
		"""
		if data is None:
			data = self.data
		data = data.astype(float) / 255
		data = data.clip(0, 1)

		return data

	def save(self, path: str):
		"""
		Save the data array as a image

		Parameters
		----------
		path : str
			the image path for saving

		Returns
		-------
		str
			the image path
		"""
		im = Image.fromarray(np.uint8(255 * self.data))
		im.save(path)
		return path

	def show(self):
		"""
		Show the data array as a image
		"""
		Image.fromarray(np.uint8(255 * self.data)).show()
 
	def get_data(self):
		"""
		Get the data
		"""
		return self.data

	def __repr__(self):
		"""
		String representation of the object
		"""
		return self.path
