from engine import poisson, boundary, image_handler

class blur(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a blured image.

	This contains all the functions needed to blur a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""
	def __init__(self, path, color=False):
		image_handler.ImageHandler.__init__(self, path, color)
		poisson.poisson.__init__(self)
		boundary.Boundary.__init__(self)
		if not path is None:
			self.set_boundary(self.NEUMANN)
		self.alpha: float = 0.25
		self.lambda_size: float = 0.1

	def set_lambda_size(self, lambda_size) -> None:
		"""
		Sets the lambda fro data attachment

		Parameters
		----------
		lambda_size : float
			The lambda parameter
		"""
		self.lambda_size = lambda_size
		
	def iteration(self):
		"""
		Does one iteration of the method.

		"""
		assert 0 <= self.lambda_size <= 1, "lamda is out of scope [0, 1]"
		self.verify_integrity()


		# TODO : Seems like data attachment works, but it still "flickers" after some iterations, figure out why 

		h = lambda x=None, i=None: (self.common_shape(self.lambda_size * (self.data - self.data_copy))) if i is None else (self.common_shape(self.lambda_size * (self.data[:, :, i] - self.data_copy[:, :, i])))
		operator = lambda i=None: self.get_laplace(self.data) if i is None else self.get_laplace(self.data[:, :, i])

		self.data = self.solve(self.data,operator, h).clip(0, 1) 

		# TODO : Make user have the option to choose
		#self.data = self.neumann(self.data)

		return self.data

	def fit(self, epochs):
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


