import image_handler
import poisson
import boundary
import numpy as np
from PIL import Image


#   TODO: Add support for "data attachment"

class blur(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
	"""
	This class describes a blured image.
	"""
    def __init__(self, path, color=False):
        """
        Defines a (blured) image

        This contains all the functions needed to blur a image over multiple iterations

        Parameters
        ----------
        path : str
            path to a image file
        color : bool
            if the image should be shown with colors
        """
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        boundary.Boundary.__init__(self)
        self.alpha = 0.25
        
    def iteration(self):
        """
        Does one iteration of the method.

        """
        laplace = self.get_laplace()
        self.data[1:-1, 1:-1] += self.alpha * laplace
        self.data = self.neumann(self.data)
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
