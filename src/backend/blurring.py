import image_handler
import poisson
import boundary
import numpy as np
from PIL import Image


#   TODO: Add support for "data attachment"

class blur(image_handler.ImageHandler, poisson.poisson, boundary.Boundary):
    def __init__(self, path, color=False):
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        boundary.Boundary.__init__(self)
        self.alpha = 0.25
        
    def iteration(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        laplace = self.get_laplace()
        self.data[1:-1, 1:-1] += self.alpha * laplace
        self.data = self.neumann(self.data)
        return self.data

    def fit(self,epochs):
        """
        [TODO:summary]

        [TODO:description]

        Parameters
        ----------
        epochs : int
            The iteration count
        """
        for i in range(epochs):
            self.iteration()
        return self
