from PIL import Image
import numpy as np

class ImageLoader:
    def __init__(self, path):
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

  #      self.covert_single_shape()
   #     self.convert_black_and_white()
        
        self.convert_color()
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

    def convert_black_and_white(self, data=None):
        """
        [TODO:summary]

        [TODO:description]
        """
        if(data is None):
            return self.data
        data[data < 0] = 0
        data[1 < data] = 1
        return data


    def get_data():
        """
        [TODO:summary]

        [TODO:description]
        """
        return self.image_data





