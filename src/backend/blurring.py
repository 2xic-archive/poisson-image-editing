from __future__ import annotations

from nptyping import Array

from engine import poisson, boundary, image_handler


class Blur(image_handler.ImageHandler, poisson.Poisson, boundary.Boundary):
    """
    This class describes a blurred image.

    This contains all the functions needed to blur a image over multiple iterations
    """

    def __init__(self, path, color=False):
        """
        Constructs a new instance of the Blur object.

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
        if not path is None:
            self.set_boundary(self.NEUMANN)
        self.alpha: float = 0.25
        self.lambda_size: float = 0

    def set_lambda_size(self, lambda_size) -> None:
        """
        Sets the lambda fro data attachment

        Parameters
        ----------
        lambda_size : float
            The lambda parameter
        """
        self.lambda_size = lambda_size

    def iteration(self) -> Array:
        """
        Does one iteration of the method.

        Returns
        -------
        ndarray
            The numpy array with the new image after the iteration
        """
        assert 0 <= self.lambda_size <= 1, "lamda is out of scope [0, 1]"
        self.verify_integrity()
        self.data = self.solve(self.data, self.opeartor, self.h)
        return self.data

    def opeartor(self, i=None) -> Array:
        """
        Solves the "u"(gradient) part of the Poisson equation

        Parameters
        ----------
        i : int
            The channel to "work" on

        Returns
        -------
        ndarray
            The u value
        """
        if i is None:
            return self.get_laplace(self.data, alpha=True)
        else:
            return self.get_laplace(self.data[:, :, i], alpha=True)

    def h(self, i=None) -> Array:
        """
        Solves the "h" part of the Poisson equation

        Parameters
        ----------
        i : int
            The channel to "work" on

        Returns
        -------
        ndarray
            The h value
        """
        if i is None:
            return self.common_shape(self.lambda_size * (self.data - self.data_copy))
        else:
            return self.common_shape(self.lambda_size * (self.data[:, :, i] - self.data_copy[:, :, i]))

    def fit(self, epochs) -> Blur:
        """
        Makes multiple iterations of the method

        Calls iteration as many times as specified in by the parameter epochs

        Parameters
        ----------
        epochs : int
            The iteration count

        Returns
        -------
        Blur
            Returns self
        """
        for i in range(epochs):
            self.iteration()
        return self
