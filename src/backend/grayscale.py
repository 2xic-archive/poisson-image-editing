from __future__ import annotations

import numpy as np
from nptyping import Array

from engine import boundary
from engine import image_handler
from engine import poisson


class Grayscale(image_handler.ImageHandler, poisson.Poisson, boundary.Boundary):
    """
    This class describes a grayscaled image.

    This contains all the functions needed to make a color image into a grayscaled image over multiple iterations
    """

    def __init__(self, path, color=True):
        """
        Constructs a new instance of the Grayscale object.

        Parameters
        ----------
        path : str
            Path to a image file
        color : bool
            If the image should be shown with colors
        """
        assert color == True, "we can only grayscale images that have color"

        image_handler.ImageHandler.__init__(self, path, color)
        poisson.Poisson.__init__(self)
        boundary.Boundary.__init__(self)

        self.mode_boundary = "neumann"

        self.avg = self.data.copy().mean(axis=2)
        self.results = np.zeros((self.data.shape[:2]))

    def reset(self):
        """
        Reset the method
        """
        self.data = self.data_copy.copy()

    def h_func(self) -> Array:
        """
        The h variable of the Poisson equation

        Returns
        -------
        ndarray
            The h value array
        """
        g_length = np.sum(self.get_gradient_norm(self.data_copy[:, :, i]) for i in range(3)) / np.sqrt(3)
        rgb_sum = np.sum(self.data_copy[:, :, i] for i in range(self.data_copy.shape[-1]))
        rgb_sx, rgb_sy = self.get_gradient(rgb_sum)

        length = np.sqrt(rgb_sx ** 2 + rgb_sy ** 2)
        length[length == 0] = np.finfo(float).eps

        rgb_sx /= length
        rgb_sy /= length

        h_prime_x, h_prime_y = rgb_sx * g_length, rgb_sy * g_length

        h_sx, _ = self.get_gradient(h_prime_x)
        _, h_sy = self.get_gradient(h_prime_y)

        return (h_sx + h_sy)

    def iteration(self) -> None:
        """
        Does one iteration of the method.

        Returns
        -------
        ndarray
            The new image array
        """
        self.verify_integrity()

        #	Reset the dimension on first round
        if len(np.shape(self.data)) == 3:
            self.data = self.data.mean(axis=2)
            self.h_array = self.h_func()

        self.data = self.solve(self.data, self.opeartor, self.h, apply_boundary=False)
        return self.data

    def opeartor(self) -> Array:
        """
        Solves the "u" part of the Poisson equation

        Returns
        -------
        ndarray
            The u value
        """
        return self.get_laplace(self.data, alpha=False)

    def h(self) -> Array:
        """
        Solves the "h" part of the Poisson equation

        Returns
        -------
        ndarray
            The h value
        """
        return self.common_shape(self.h_array)

    def fit(self, epochs) -> Grayscale:
        """
        Makes multiple iterations of the method

        Calls iteration as many times as specified in by the parameter epochs

        Parameters
        ----------
        epochs : int
            The iteration count

        Returns
        -------
        Grayscale
            Returns self
        """
        for _ in range(epochs):
            self.iteration()
        return self
