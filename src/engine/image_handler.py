import numpy as np
from PIL import Image
from nptyping import Array


class ImageHandler:
    """
    This class describes the abstracts functions for a image
    """

    def __init__(self, path: str = None, color: bool = True):
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
            self.color = color
            image = Image.open(path)
            image.load()
            self.process(image)
            '''
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
            '''

    def resize(self, scale=8):
        im = Image.open(self.path)
        width, height = im.size
        im = im.resize((width//scale, height//scale))
        self.process(im)

    def process(self, image):
        self.data = np.asarray(image, dtype="float64").copy()
        if not self.color and not len(self.data.shape) == 2:
            self.data = self.covert_single_shape()
            self.data = self.convert_black_and_white()
        else:
            self.data = self.convert_color()
        self.data_copy = self.data.copy()

    def set_data(self, data: Array):
        """
        [TODO:summary]

        [TODO:description]
        """
        self.data = data
        self.data_copy = self.data.copy()

    def reset(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        self.data = self.data_copy.copy()

    def get_gradient_norm(self, data: Array = None) -> Array[float]:
        """
        [TODO:summary]

        [TODO:description]
        """
        if data is None:
            data = self.data
        #   https://stackoverflow.com/questions/38809852/can-i-use-numpy-gradient-function-with-images
        gx, gy = self.get_gradient(data)
        return np.sqrt(gx ** 2 + gy ** 2)

    def get_gradient(self, data: Array) -> Array:
        """
        [TODO:summary]

        [TODO:description]
        """
        if data is None:
            data = self.data
        gx, gy = np.gradient(data, axis=[0, 1])
        return gx, gy

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
        """
        [TODO:summary]

        [TODO:description]
        """
        if data is None:
            data = self.data
        data = data.astype(float) / 255
        data[data < 0] = 0
        data[1 < data] = 1
        return data

    def add_noise(self, noise_level: float = 0.05):
        """
        [TODO:summary]

        [TODO:description]
        """
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

    def save(self, name: str):
        """
        [TODO:summary]

        [TODO:description]
        """
        im = Image.fromarray(np.uint8(255 * self.data))
        im.save(name)
        return name

    def show(self):
        Image.fromarray(np.uint8(255 * self.data)).show()
      #  Image.fromarray((255 * self.data)).show()

    def get_data(self):
        """
		[TODO:summary]

		[TODO:description]
		"""
        return self.data

    def __repr__(self):
        return self.path
