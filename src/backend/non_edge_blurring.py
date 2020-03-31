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

    def D(self, k=300) -> Array:
        fraction = 1 / \
                   (1 + k * (self.get_gradient_norm(self.data_copy)) ** 2)
        return fraction

    def iteration(self) -> Array: 
        """
		Does one iteration of the method.

		"""
        D = self.D()
        assert np.all(D <= 1), "D function error" 

        d_x, d_y = self.get_gradient(D)
        data_x, data_y = self.get_gradient(self.data)
        combined = (d_x  + d_y)

        #  Maybe I need to create a new numerical scheme for implicit ? 
        #   however since g*(D*g(u)),d=1 -> is the same as g^2u-h, with h=0, should be able to exploit the OG equation ? 
        D[:, :] = 1

        operator = lambda i=None: (self.get_laplace(self.data) * self.common_shape(D) ) + (self.common_shape(combined) * self.alpha) 
        self.data = self.solve(self.data,operator)#, h)#.clip(0, 1) 
   #     self.data = self.neumann(self.data).clip(0, 1)
        
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
