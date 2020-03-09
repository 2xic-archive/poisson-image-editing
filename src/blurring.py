import loader
import numpy as np
from PIL import Image
class blur(loader.ImageLoader):
    def __init__(self, path, color=False):
        loader.ImageLoader.__init__(self, path)
        
        self.color = color
        
        if not color:
            self.data = self.covert_single_shape()
            self.data = self.convert_black_and_white()    
        else:
  #          self.data = self.covert_single_shape()
            self.data = self.convert_color()    
        self.alpha = 0.25
        
    def eksplisitt(self):
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
            self.eksplisitt()
        return self

    def save(self, name):
        from PIL import Image
        im = Image.fromarray(np.uint8(self.data))
        im.save(name)
        return name