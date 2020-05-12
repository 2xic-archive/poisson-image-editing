from __future__ import annotations

import numpy as np
from nptyping import Array

from engine import image_handler
from engine import poisson, boundary


class Contrast(image_handler.ImageHandler, poisson.Poisson, boundary.Boundary):
    """
    This class describes a contrast image.

    This contains all the functions needed to improve the contrast of a image over multiple iterations
    """

    def __init__(self, path, color=False):
        """
        Constructs a new instance of the Contrast object.

        Parameters
        ----------
        path : str
            path to a image file
        color : bool
            if the image should be shown with colors
        """
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.Poisson.__init__(self)
        boundary.Boundary.__init__(self, self.data.copy())

        self.k = 10
        self.mode_boundary = "neumann"

    def calculate_h(self):
        """
        Builds the array for the "h" part of the Poisson equation
        """
        if len(self.data_copy.shape) == 2:
            self.h_arr = self.k * self.get_laplace(np.copy(self.data_copy), alpha=True)
        else:
            self.h_arr = self.k * (np.asarray([self.get_laplace(np.copy(self.data_copy[:, :, i]))
                                               for i in range(self.data_copy.shape[-1])]))

    @property
    def k(self) -> float:
        """
        Returns the k variable
        """
        return self._k

    @k.setter
    def k(self, k):
        """
        Sets the k variable

        Will also automatically calculate the new h array

        Parameters
        -------
        k
            the the new k value
        """
        assert type(k) == float or type(k) == int, "k should be a number"
        self._k = k
        self.calculate_h()

    def iteration(self) -> Array:
        """
        Does one iteration of the method.

        Returns
        -------
        array
            the new image array
        """
        self.verify_integrity()

        self.data = self.solve(self.data, self.operator, self.h)
        return self.data

    def operator(self, i=None) -> Array:
        """
        Solves the "u" part of the Poisson equation

        Returns
        -------
        array
            the u value
        """
        if i is None:
            return self.get_laplace(self.data, alpha=True)
        else:
            return self.get_laplace(self.data[:, :, i], alpha=True)

    def h(self, i=None) -> Array:
        """
        Solves the "h" part of the Poisson equation

        Returns
        -------
        array
            the h value
        """
        if len(self.h_arr.shape) == 3:
            return self.h_arr[i, :, :]
        else:
            return self.h_arr

    def fit(self, epochs=1) -> Contrast:
        """
        Makes multiple iterations of the method

        Calls iteration as many times as specified in by the parameter epochs

        Parameters
        ----------
        epochs : int
            The iteration count

        Returns
        -------
        Contrast
            returns self
        """
        for i in range(epochs):
            self.iteration()
        return self
