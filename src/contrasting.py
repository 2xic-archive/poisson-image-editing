import loader
import numpy as np
from PIL import Image
class contrast(loader.ImageLoader):
    def __init__(self, path, color=False):
        loader.ImageLoader.__init__(self, path, color)
        self.alpha = 0.25
        self.k = 1
        self.u0 = np.copy(self.data)
    
    def eksplisitt(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        laplace = self.get_laplance()
        self.data[1:-1, 1:-1] += (self.u0[1:-1, 1:-1] - (self.k * laplace)) * self.alpha
     						   # ((laplace) - (self.k * self.u0[1:-1, 1:-1])) * self.alpha <- guess i had it backwards?
     						   #	TODO: check if this is correct. 
        self.data.clip(0, 1)

        #(self.u0 - (laplace


        """
        TODO : Implement Neumann
        """
#        self.data[:, 0] = self.data[:, 1]      # Neumann randbetingelse
#        self.data[:, -1] = self.data[:, -2]    #
#        self.data[0, :] = self.data[1, :]      #
#        self.data[-1, :] = self.data[-2 , :]   #

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
            self.eksplisitt()
        return self