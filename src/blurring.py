import image_handler
import poisson
import numpy as np
from PIL import Image

class blur(image_handler.ImageHandler, poisson.poisson):
    def __init__(self, path, color=False):
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        self.alpha = 0.25
        
    def iteration(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        laplace = self.get_laplance()
        self.data[1:-1, 1:-1] += self.alpha * laplace

        self.data[:, 0] = self.data[:, 1]      # Neumann randbetingelse
        self.data[:, -1] = self.data[:, -2]    #
        self.data[0, :] = self.data[1, :]      #
        self.data[-1, :] = self.data[-2 , :]   #

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
