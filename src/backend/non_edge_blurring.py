from __future__ import annotations

import numpy as np
from nptyping import Array

from engine import boundary
from engine import image_handler
from engine import poisson


class NonEdgeBlur(image_handler.ImageHandler, poisson.Poisson, boundary.Boundary):
    """
    This class describes a edge edge preserving blurred image.

    This contains all the functions needed to preform a edge preserving blur on a image over multiple iterations
    """

    def __init__(self, path, color=False):
        """
        Constructs a new instance of the NonEdgeBlur object.

        Parameters
        ----------
        path : str
            Path to a image file
        color : bool
            If the image should be shown with colors
        """

        image_handler.ImageHandler.__init__(self, path, color)
        poisson.Poisson.__init__(self)
        boundary.Boundary.__init__(self)
        self.k = 1000

    @property
    def k(self):
        """
        Returns the k variable
        """
        return self._k

    @k.setter
    def k(self, k):
        """
        Sets the k variable

        Will also create the D function gradient array

        Parameters
        -------
        k
            The the new k value
        """
        assert type(k) == float or type(k) == int, "k should be a number"
        self._k = k
        self.set_D_gradient()

    def D(self) -> Array:
        """
        The D function

        Returns
        -------
        ndarray
            The new D array
        """
        fraction = 1 / \
                   (1 + self.k * (self.get_gradient_norm(self.data_copy)) ** 2)
        return fraction

    def set_D_gradient(self):
        """
        Calculates the gradient array (for x and y) of the D function

        """
        self.D_arr = self.D()
        assert np.all(self.D_arr <= 1), "D function error"

        self.d_xy = np.asarray(self.get_gradient(self.D_arr))

    def iteration(self) -> Array:
        """
        Does one iteration of the method.

        Returns
        -------
        ndarray
            The new image array
        """
        self.data = self.solve(self.data, self.operator)
        return self.data

    def operator(self, i=None):
        """
        Solves the "u" part of the Poisson equation

        Parameters
        ----------
        i : int
            The channel to "work" on
        """
        data_xy = np.asarray(self.get_gradient(self.data))
        combined = np.sum(self.d_xy * data_xy, axis=0)
        if i is None:
            return (self.common_shape(self.D_arr) * self.get_laplace(self.data, alpha=False)
                     + self.common_shape(combined))
        else:
            return (self.common_shape(self.D_arr)[:, :, i] * self.get_laplace(self.data[:, :, i], alpha=False)
                     + self.common_shape(combined[:, :, i]))

    def fit(self, epochs) -> NonEdgeBlur:
        """
        Makes multiple iterations of the method

        Calls iteration as many times as specified in by the parameter epochs

        Parameters
        ----------
        epochs : int
            The iteration count

        Returns
        -------
        NonEdgeBlur
            Returns self
        """
        for i in range(epochs):
            self.iteration()
        return self
