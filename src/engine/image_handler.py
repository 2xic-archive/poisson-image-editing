import numpy as np
from PIL import Image


class ImageHandler:
    """
    This class describes the abstracts functions for a image
    """
    def __init__(self, path=None, color=True):
        """
		[TODO:summary]

		[TODO:description]

		Parameters
		----------
		path : String
			[TODO:description]
		"""
        if not path is None:
            self.path = path
            image = Image.open(path)
            image.load()
            self.data = np.asarray(image, dtype="float64").copy()
            if not color and not len(self.data.shape) == 2:
                self.data = self.covert_single_shape()
                self.data = self.convert_black_and_white()
            else:
                self.data = self.convert_color()
            self.data_copy = self.data.copy()
            self.color = color

    def set_data(self, data):
        self.data = data

    def reset(self):
        self.data = self.data_copy.copy()

    def get_gradient(self, data=None):
        if(data is None):
            data = self.data
        #   https://stackoverflow.com/questions/38809852/can-i-use-numpy-gradient-function-with-images
        gx, gy = np.gradient(data)
        return np.sqrt(gx ** 2 + gy ** 2)

    def covert_single_shape(self, data=None):
        """
		[TODO:summary]

		[TODO:description]
		"""
        if data is None:
            data = self.data
        data = np.sum(data.astype(float), 2) / (3 * 255)
        # return self.data
        return data

    def convert_color(self, data=None):
        if data is None:
            data = self.data
        data = data.astype(float) / 255
        data[data < 0] = 0
        data[1 < data] = 1
        return data

    def add_nosise(self, noise_level=0.05):
        self.data = self.data + noise_level * np.random.randn(*self.data.shape)
        self.data[self.data < 0] = 0
        self.data[1 < self.data] = 1

    def convert_black_and_white(self, data=None):
        """
		[TODO:summary]

		[TODO:description]
		"""
        if data is None:
            data = self.data
        data[data < 0] = 0
        data[1 < data] = 1
        return data

    def save(self, name):
        im = Image.fromarray(np.uint8(self.data))
        im.save(name)
        return name

    def get_data(self):
        """
		[TODO:summary]

		[TODO:description]
		"""
        return self.data

    def __repr__(self):
        return self.path
