from PIL import Image
import numpy as np

class ImageLoader:
    def __init__(self, path, color=True):
        """
        [TODO:summary]

        [TODO:description]

        Parameters
        ----------
        path : String
            [TODO:description]
        """
        image = Image.open(path)
        image.load()
        self.data = np.asarray(image, dtype="float64").copy()#, dtype="inter")

        if not color and not len(self.data.shape) == 2:
            self.data = self.covert_single_shape()
            self.data = self.convert_black_and_white()    
        else:
  #          self.data = self.covert_single_shape()
            self.data = self.convert_color()    
        self.color = color
  #      self.covert_single_shape()
   #     self.convert_black_and_white()
        
 #       self.convert_color()
#        self.data[self.data < 0] = 0
 #       self.data[1 < self.data] = 1
    
    def covert_single_shape(self, data=None):
        """
        [TODO:summary]

        [TODO:description]
        """
        if(data is None):
            data = self.data
        data = np.sum(data.astype(float), 2) / (3 * 255)
        #return self.data
        return data

    def convert_color(self, data=None):
        if(data is None):
            data = self.data
        data = data.astype(float) / 255
        data[data < 0] = 0
        data[1 < data] = 1
        return data

    def add_nosise(self, noise_level=0.05):
        self.data = self.data + noise_level *np.random.randn(*self.data.shape)
        self.data [self.data  < 0] = 0
        self.data [1 < self.data ] = 1

    def convert_black_and_white(self, data=None):
        """
        [TODO:summary]

        [TODO:description]
        """
        if(data is None):
            data = self.data
        data[data < 0] = 0
        data[1 < data] = 1
        return data

    def get_laplance(self, data=None):
        if(data is None):
            data = self.data
        laplace = data[0:-2, 1:-1] \
                + data[2:, 1:-1] \
                + data[1:-1, 0:-2] \
                + data[1:-1, 2:]   \
                - 4 * data[1:-1, 1:-1]
        return laplace

    def get_data(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        return self.data





