from engine import image_handler
import numpy as np
from engine import poisson
from nptyping import Array

class inpaint(image_handler.ImageHandler, poisson.poisson):
    """
	This class describes a inpaited image.

	This contains all the functions needed to inpait a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""
    mode: str
    alpha: float

    def __init__(self, path: str, color: bool = False):
        if not path is None:
            image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)

        self.alpha = 0.25
        self.mask = None
        self.copy = None
        self.mode = "inpait"

    def set_demosaicing(self) -> None:
        self.mode = "demosaicing"
        
    def set_data(self, data) -> None:
        """
		Sets the data used by the class

		Parameters
		----------
		data : ndarray
			sets the data
		"""
        self.data = data

    def set_mask(self, mask) -> None:
        """
		Sets the mask used by the class

		Parameters
		----------
		mask : ndarray
			sets the mask
		"""
        self.mask = mask

    def set_orignal(self, original) -> None:
        """
		Sets the original verison of the data used by the class

		Parameters
		----------
		original : ndarray
			sets the original
		"""
        self.original_data = original

    def destroy_information(self, strength=2) -> Array:
        """
		Destroys parts of the image

		Parameters
		----------
		strength : int
			a number from 1 to 10, this is used to set the level of noise added
		"""
        noise = np.random.randint(0, 10, size=self.data.shape)
        mask = np.zeros(self.data.shape)

        mask[strength < noise] = 1
        mask[noise < strength] = 0
        #		print(mask)
        self.data *= mask
        self.mask = mask
        self.original_data = np.copy(self.data)
        return mask

    def iteration(self) -> None:
        """
		Does one iteration of the method.

		"""
        laplace = self.get_laplace(self.data)
        self.data[1:-1, 1:-1] += self.alpha * laplace
        """
		mask content
			original value = 1 
			infomation lost = 0 
		"""
        """
			TODO: Figure out what is wrong here
		"""
        if (self.mode == "inpait"):
            self.data = (self.data * (1 - self.mask)) + (self.original_data * (self.mask))
        else:
            self.data = (self.data * (self.mask)) + abs(self.original_data * (1 - self.mask))

    def fit(self, original=None, data=None, mask=None, epochs:int=1) -> Array:
        """
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		original : ndarray
			The original version of the image
		data : ndarray
			Set current data (TODO : MAKE BETTER NAME)
		mask : ndarray
			Set mask of the image
		epochs : int
			The iteration count
		"""
        if not mask is None:
            self.set_mask(mask)
        if not original is None:
            self.set_orignal(original)
        if not data is None:
            self.set_data(data)
        if (self.mask is None):
            raise Exception("You need to set a mask")

        for i in range(epochs):
            self.iteration()
        return self.data
