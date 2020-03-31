from engine import image_handler, boundary
import numpy as np
from engine import poisson
from nptyping import Array

class inpaint(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a inpaited image.

	This contains all the functions needed to inpait a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""
	mode: str
	alpha: float

	def __init__(self, path: str, color: bool = False):
		if not path is None:
			image_handler.ImageHandler.__init__(self, path, color)
			boundary.Boundary.__init__(self, self.data.copy())
		else:
			boundary.Boundary.__init__(self)

		poisson.poisson.__init__(self)

		self.alpha = 0.25
		self.mask = None
		self.copy = None
		self.mode = "inpait"

	def set_demosaicing(self) -> None:
		self.mode = "demosaicing"
		
	def set_data(self, data) -> None:
		"""
		Sets the data used by the class

		Parameters
		----------
		data : ndarray
			sets the data
		"""
		self.data = data
		#self.u0 = 
		#self.data.copy()
	 #   self.set_u0(self.data.copy())

	def set_mask(self, mask) -> None:
		"""
		Sets the mask used by the class

		Parameters
		----------
		mask : ndarray
			sets the mask
		"""
		self.mask = mask

	def set_orignal(self, original) -> None:
		"""
		Sets the original verison of the data used by the class

		Parameters
		----------
		original : ndarray
			sets the original
		"""
		self.original_data_copy = original

	def destroy_information(self, strength=2) -> Array:
		"""
		Destroys parts of the image

		Parameters
		----------
		strength : int
			a number from 1 to 10, this is used to set the level of noise added
		"""
		noise = np.random.randint(0, 10, size=self.data.shape[:2])
		mask = np.zeros(self.data.shape[:2])

		mask[strength < noise] = 1
		mask[noise < strength] = 0
		#		print(mask)
		if(len(self.data.shape) == 3 ):
			for i in range(self.data.shape[-1]):
				 self.data[:, :, i] *= mask
		else:
			self.data *= mask

		self.mask = mask
		self.original_data_copy = np.copy(self.data)
		return mask

	def iteration(self) -> None:
		"""
		Does one iteration of the method.

		"""
		operator = lambda i=None: self.get_laplace(self.data) if i is None else (self.get_laplace(self.data[:, :, i]))

		"""
		mask content
			original value = 1 
			infomation lost = 0 
		"""
		response = self.solve(self.data, operator)
		if(len(self.data.shape) == 3):
			for i in range(self.data.shape[-1]):
				self.data[:, :, i] = (response[:, :, i] * (1 - self.mask)) + (self.original_data_copy[:, :, i] * (self.mask))
		else:
			self.data = (self.data * (1 - self.mask)) + (self.original_data_copy * (self.mask))
			
		self.data = self.neumann(self.data)


	def fit(self, original=None, data=None, mask=None, epochs:int=1) -> Array:
		"""
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		original : ndarray
			The original version of the image
		data : ndarray
			Set current data (TODO : MAKE BETTER NAME)
		mask : ndarray
			Set mask of the image
		epochs : int
			The iteration count
		"""
		if not mask is None:
			self.set_mask(mask)
		if not original is None:
			self.set_orignal(original)
		if not data is None:
			self.set_data(data)
		if (self.mask is None):
			raise Exception("You need to set a mask")

		for i in range(epochs):
			self.iteration()
		return self.data
