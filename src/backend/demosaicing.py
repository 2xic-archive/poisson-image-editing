from __future__ import annotations
from engine import image_handler
from engine import poisson
import numpy as np
from backend import inpaiting


class Demosaic(image_handler.ImageHandler, poisson.poisson):
    """
	This class describes a demosaic image.

	This contains all the functions needed to perform demosaic on a image over multiple iterations

	Parameters
	----------
	path : str
		path to a image file
	color : bool
		if the image should be shown with colors
	"""

    def __init__(self, path: str, color: bool = True):
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        self.alpha = 0.25
        self.inpaint = inpaiting.inpaint(None)

        self.simulate()
        self.inpaint.data = self.mosaic

        self.results = np.zeros(self.mosaic.shape + (3,))
        self.results[:, :, 0] = self.mosaic
        self.results[:, :, 1] = self.mosaic
        self.results[:, :, 2] = self.mosaic

    def reset(self):
        self.data = self.data_copy.copy()
        self.simulate()
        self.inpaint.data = self.mosaic        

    def simulate(self):
        """
		Simualtes a image into a state where we can preform demosaic

		"""

        u = self.data
        self.mosaic = np.zeros(u.shape[:2])  # Alloker plass
        self.mosaic[::2, ::2] = u[::2, ::2, 0]  # R-kanal
        self.mosaic[1::2, ::2] = u[1::2, ::2, 1]  # G-kanal
        self.mosaic[::2, 1::2] = u[::2, 1::2, 1]  # G-kanal
        self.mosaic[1::2, 1::2] = u[1::2, 1::2, 2]  # B-kanal

        self.rgb_mosaic = np.zeros(self.mosaic.shape + (3,))
        self.rgb_mosaic[:, :, 0] = self.mosaic[:, :]
        self.rgb_mosaic[:, :, 1] = self.mosaic[:, :]
        self.rgb_mosaic[:, :, 1] = self.mosaic[:, :]
        self.rgb_mosaic[:, :, 2] = self.mosaic[:, :]

        self.mask = np.ones(np.shape(self.mosaic) + (3,))
        self.mask[::2, ::2, 0] = 0
        self.mask[1::2, ::2, 1] = 0
        self.mask[::2, 1::2, 1] = 0
        self.mask[1::2, 1::2, 2] = 0

        return self.mosaic

    def iteration(self) -> None:
        """
		Does one iteration of the method.

		"""
        self.inpaint.alpha = 0.05
        self.inpaint.set_demosaicing()

        operator = lambda i: self.inpaint.fit(self.rgb_mosaic[:, :, i], self.results[:, :, i],
                                                     self.mask[:, :, i])#self.get_laplace(self.data)
        self.data = self.solve(self.results, operator) 

        '''
        for i in range(3):
            self.results[:, :, i] = self.inpaint.fit(self.rgb_mosaic[:, :, i], self.results[:, :, i],
                                                     self.mask[:, :, i])
        '''
        self.data = self.results

    def fit(self, epochs: int = 1) -> Demosaic:
        """
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count
		"""
        for i in range(epochs):
            self.iteration()
        return self
