from __future__ import annotations
from engine import image_handler
from engine import poisson
from engine import boundary
import numpy as np
from PIL import Image
from nptyping import Array
import numpy as np

class non_edge_blur(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a edge edge preserving blurred image.

	This contains all the functions needed to preform a edge preserving blur on a image over multiple iterations

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
		self.alpha = 0.1
#        self.mode_poisson = self.EXPLICIT

		self.set_u0(self.data.copy())

	def D(self, k=1000) -> Array:
		"""
		The D function 
		"""
		fraction = 1 / \
				   (1 + k * (self.get_gradient_norm(self.data_copy)) ** 2)
		return fraction

	def iteration(self) -> Array: 
		"""
		Does one iteration of the method.

		"""
		D = self.D()
		assert np.all(D <= 1), "D function error" 

		d_xy = np.asarray(self.get_gradient(D))
		data_xy = np.asarray(self.get_gradient(self.data))
		combined = np.sum(d_xy * data_xy, axis=0)
        
		operator = lambda i=None: (self.alpha * \
					(self.common_shape(D) * self.get_laplace_explicit(self.data, alpha=False) +  self.common_shape(combined))
		)
		self.data = self.solve(self.data, operator).clip(0, 1)

		return self.data

	def fit(self, epochs) -> non_edge_blur:
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
