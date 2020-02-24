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

        #self.covert_single_shape()
        #self.convert_black_and_white()
        self.convert_color()
        self.data[self.data < 0] = 0
        self.data[1 < self.data] = 1
    
    def covert_single_shape(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        self.data = np.sum(self.data.astype(float), 2) / (3 * 255)
        #return self.data

    def convert_color(self):
        self.data = self.data.astype(float) / 255
        self.data[self.data < 0] = 0
        self.data[1 < self.data] = 1

    def convert_black_and_white(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        self.data[self.data < 0] = 0
        self.data[1 < self.data] = 1

    def get_data():
        """
        [TODO:summary]

        [TODO:description]
        """
        return self.image_data


