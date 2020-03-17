import image_handler
import poisson
import numpy as np
from PIL import Image

class grayscale(image_handler.ImageHandler, poisson.poisson):
    def __init__(self, path, color=True):
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        self.alpha = 0.25

   
    def iteration(self):
        """
        [TODO:summary]

        [TODO:description]
        """

        # TODO : Remove need for scipy
        from scipy import ndimage
        sx = ndimage.sobel(self.data, axis=0, mode='constant')
        sy = ndimage.sobel(self.data, axis=1, mode='constant')

        g = np.sqrt(sx ** 2 + sy ** 2)/np.sqrt(3)
            
        self.data  = sx

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
