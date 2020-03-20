# TODO : http://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf
import image_handler
import poisson
import boundary
import numpy as np
from PIL import Image


class hdr_reconstruction(image_handler.ImageHandler, poisson.poisson):
    def __init__(self, path, color=False):
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        self.alpha = 0.25
        
    def iteration(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        raise Exception("implement")
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
