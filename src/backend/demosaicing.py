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
        self.simulated = False
   #     self.simulate()

    def reset(self):
        self.data = self.data_copy.copy()
        #self.simulate()
        self.simulated = False
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

        self.mask = np.zeros(np.shape(self.mosaic) + (3,))
        self.mask[::2, ::2, 0] = 1
        self.mask[1::2, ::2, 1] = 1
        self.mask[::2, 1::2, 1] = 1
        self.mask[1::2, 1::2, 2] = 1

        self.inpaint.data = self.mosaic.copy()

        self.results = np.zeros(self.mosaic.shape + (3,))
        self.results[:, :, 0] = self.mosaic
        self.results[:, :, 1] = self.mosaic
        self.results[:, :, 2] = self.mosaic

        self.simulated = True
        self.data = self.mosaic

        return self.mosaic

    def iteration(self) -> None:
        """
		Does one iteration of the method.

		"""
        self.inpaint.alpha = 0.05
        operator = lambda i: self.inpaint.fit(self.rgb_mosaic[:, :, i], self.results[:, :, i], self.mask[:, :, i])
        self.data = self.solve(self.results, operator) 

        '''
        for i in range(3):
            self.results[:, :, i] = self.inpaint.fit(self.rgb_mosaic[:, :, i], self.results[:, :, i],
                                                     self.mask[:, :, i])
        '''
        self.data = self.results.copy()

    def fit(self, epochs: int = 1) -> Demosaic:
        """
		Makes multiple iterations of the method

		Calls iteration as many times as spesifed in by the parameter epochs

		Parameters
		----------
		epochs : int
			The iteration count
		"""
        if not self.simulated:
            raise Exception("You have to simulate the mosaic first")

        for i in range(epochs):
            self.iteration()
        return self
