from __future__ import annotations
from engine import image_handler
from engine import poisson
from engine import boundary
import numpy as np
from PIL import Image
from nptyping import Array


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
        self.alpha = 0.25

    def D(self, k=25) -> Array:
        fraction = 1 / \
                   1 + k * (self.get_gradient_norm(self.data_copy)) ** 2
        return fraction

    def iteration(self) -> Array: 
        """
		Does one iteration of the method.

		"""
        laplace = self.get_laplace()

        d_x, d_y = self.get_gradient(self.D())
        combined = (d_x + d_y)[1:-1, 1:-1]

        data_x, data_y = self.get_gradient(self.data)
        combined *= (data_x + data_y)[1:-1, 1:-1]

        self.data[1:-1, 1:-1] += (self.alpha * (laplace * self.D()[1:-1, 1:-1]) + combined).clip(0, 1)
        self.data = self.neumann(self.data).clip(0, 1)

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
