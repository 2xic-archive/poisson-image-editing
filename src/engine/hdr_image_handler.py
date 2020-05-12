import os
import re

import numpy as np
from nptyping import Array


# as defined in equation 3
def classic_weight_function(intensity: float) -> float:
    """
    Basic way of weighing the intensity
    """
    if intensity <= 128:
        return intensity
    return 255 - intensity


def get_numbers(path) -> list:
    """
    Get the number from the string

    Used for getting the correct **
    """
    array = re.findall(r'[0-9]+', os.path.basename(path))
    return array


class hdr_handler:
    """
    This class describes how to handle HDR images.
    """

    def __init__(self, images, user_defined_weight_fuction=classic_weight_function):
        """
        Constructs a new instance of the hdr_handler object.

        Parameters
        ----------
        images : list
            a list of images to create a HDR from
        user_defined_weight_fuction : callable
            if you want to use a custom weight function
        """
        self.weight_function = user_defined_weight_fuction

        if user_defined_weight_fuction == classic_weight_function:
            assert (self.weight_function(128) == 128)
            assert (self.weight_function(129) == 126)

        self.images = images

        for i in range(len(self.images)):
            self.images[i].data = (255 * self.images[i].data).astype(np.uint8).astype(
                np.float64)

        self.B = np.array([
            np.log(int(get_numbers(i.path)[0])) for i in self.images
        ]
        )

        self.pixel_area = self.images[0].data.shape
        self.pixel_area = self.pixel_area[0] * self.pixel_area[1]

        # is lambda, the constant that determines the amount of smoothness
        self.lambda_constant = 100

        self.Z = self.sample()

    def normalize(self, x) -> Array:
        """
        Normalize the image with a min-max scaling

        Parameters
        ----------
        x : array
            The input (not normalized) image

        Returns
        -------
        array
            the normalized image
        """
        for i in range(x.shape[-1]):
            max_val = np.max(x[:, :, i])
            min_val = np.min(x[:, :, i])
            x[:, :, i] = (x[:, :, i] + abs(min_val)) / (max_val + abs(min_val))
        return x

    def get_pixel(self, image, sample) -> Array:
        """
        Get the pixel from the sample (x, y) in the image

        Parameters
        ----------
        image : array
            The image to sample from
        sample : array
            the location to sample from

        Returns
        -------
        array
            the image values at the sampled location
        """
        results = np.zeros(sample.shape)
        image_flat = image.flatten()
        for index, i in enumerate(sample.flatten()):
            results[:, index] = image_flat[int(i)]
        return results

    def sample(self, size=100) -> Array:
        """
        Sample pixel values from all the images

        Randomly selects pixels from all of the images as a sample

        Parameters
        ----------
        size : int
            The sample size for each image

        Returns
        -------
        array
            the sampled array for each channel and image
        """
        sample_space = np.ceil(np.random.rand(1, size) * self.pixel_area)

        Z = np.zeros((size, len(self.images), 3))
        for index, image in enumerate(self.images):
            for channel in range(3):
                Z[:, index, channel] = self.get_pixel(image.data, sample_space)
        return Z

    def get_radiance(self) -> Array:
        """
        Get the radiance of (R,G,B)

        Returns
        -------
        array
            the radiance
        """
        self.radiance = np.zeros((255, 3))
        for channel in range(3):
            g, lE = self.gsolve(self.Z[:, :, channel])
            self.radiance[:, channel] = g[:, 0]
        return self.radiance

    def get_Ab(self, Z, n=256) -> tuple:
        """
        Creates the A and b matrices

        Parameters
        ----------
        Z : array
            The sampled array
        n : int
            the color space max

        Returns
        -------
        array
            the A matrix
        array
            the b matrix
        int
            the color space max
        """
        k = 0
        A = np.zeros((Z.shape[0] * Z.shape[1] + n + 1, n + Z.shape[0]))
        b = np.zeros((A.shape[0], 1))

        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                Z_ij = int(round(Z[i, j]))
                w_ij = self.weight_function(Z_ij + 1)

                A[k, Z_ij] = w_ij
                A[k, n + i] = -w_ij

                w_ij = self.weight_function(int(Z[i, j]) + 1)
                b[k, 0] = w_ij * self.B[j]
                k += 1

        A[k, 128] = 1
        k += 1

        for i in range(0, n - 3):
            A[k, i] = self.lambda_constant * self.weight_function(i + 2)
            A[k, i + 1] = -2 * self.lambda_constant * self.weight_function(i + 2)  # + 1)
            A[k, i + 2] = self.lambda_constant * self.weight_function(i + 2)  # + 1)
            k += 1
        return A, b, n

    def gsolve(self, Z) -> tuple:
        """
        Gets the response function

        From the paper : "Given a set of pixel values observed for several pixels in several
        images with different exposure times, this function returns the
        imaging system’s response function g as well as the log film irradiance
        values for the observed pixels."


        Parameters
        ----------
        Z : array
            The sampled array of pixel values

        Returns
        -------
        array
            the response function
        array
            the "log film irradiance values for the observed pixels." - paper qoute
        """

        A, b, n = self.get_Ab(Z)

        #	using leastsq did not work
        #	https://github.com/numpy/numpy/issues/9563
        def leastsq(X, Y):
            """ Solves the problem Y = XB """
            inv = np.linalg.pinv(np.dot(X.T, X))
            cross = np.dot(inv, X.T)
            beta = np.dot(cross, Y)
            return beta

        x = leastsq(A, b)
        g = x[1:n]
        lE = x[n + 1:x.shape[0]]
        return g, lE

    def look_up_pixel(self, radiance, image) -> Array:
        """
        Check the radiance value on the (x, y) from the image

        Creates a new image based on the mapping of the response function

        Parameters
        ----------
        radiance : array
            The radiance value based on the response function
        image : array
            The image we are working on

        Returns
        -------
        array
            output image
        """
        out_image = np.zeros((image.shape))
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                out_image[i, j] = radiance[int(image[i, j]) - 1]
        return out_image

    def get_radiance_log(self, radiance) -> Array:
        """
        Equation 6 from the paper

        Parameters
        ----------
        radiance : array
            The radiance value based on the response function

        Returns
        -------
        array
            the log output
        """
        x = np.ones(self.images[0].data.shape)
        y = np.zeros(self.images[0].data.shape)

        for index, i in enumerate(self.images):
            g = i.data.copy()
            for rgb in range(3):
                g[:, :, rgb] = self.look_up_pixel(radiance[:, rgb], g[:, :, rgb])
            g -= self.B[index]

            f = np.vectorize(self.weight_function)
            wi = f(g.copy())
            x += wi * g
            y += wi
        rad = (x / y)
        return rad
