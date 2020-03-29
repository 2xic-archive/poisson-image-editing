import numpy as np
from engine import image_handler
from itertools import combinations
import scipy.io
import os
from scipy.optimize import nnls
from scipy.optimize import leastsq

"""
TODO : I now see that multiple solutions to the problem is mentioned in the project description	*awkward* will try them out
"""


# as defined in equation 3
def classic_weigth_function(intensity: float):
    """
	[TODO:summary]

	[TODO:description]
	"""
    if intensity <= 128:
        return intensity
    return 255 - intensity


class hdr_handler:
    def __init__(self, user_defined_weigth_fuction=classic_weigth_function):
        self.weigth_function = user_defined_weigth_fuction
        assert(self.weigth_function(128) == 128)
        assert(self.weigth_function(129) == 126)
        

        self.images = [
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00064.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00128.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00256.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00512.png')
        ]
     #   for i in self.images:
      #      i.resize(scale=4)

        for i in range(len(self.images)):
            self.images[i].data *= 255
            self.images[i].data = self.images[i].data.astype(np.uint8).astype(
                np.float64)

        # make sure we have all images in the correct interval between 0 and 255
        for i in range(len(self.images)):
            assert (1 < self.images[i].data.max() <= 255)

        self.B = np.array([
            np.log(64),
            np.log(128),
            np.log(256),
            np.log(512)
        ])

        self.pixel_area = self.images[0].data.shape
        self.pixel_area = self.pixel_area[0] * self.pixel_area[1]
        
        # is lamdba, the constant that determines the amount of smoothness
        self.lambda_constant = 100  

        self.Z = self.sample()

    def normalize(self, x):
        # rgb
        for i in range(x.shape[-1]):
            max_val = np.max(x[:, :, i])
            min_val = np.min(x[:, :, i])
            x[:, :, i] = (x[:, :, i] + abs(min_val))/(max_val + abs(min_val))
        return x

    def get_pixel(self, image, sample):
        """
        [TODO:summary]

        [TODO:description]
        """
        results = np.zeros(sample.shape)
        image_flat = image.flatten()
        for index, i in enumerate(sample.flatten()):
            results[:, index] = image_flat[int(i)]
        return results

    def sample(self, size=100):
        """
        [TODO:summary]

        [TODO:description]
        """
        sample_space = np.ceil(np.random.rand(1, size) * self.pixel_area)

        Z = np.zeros((size, len(self.images), 3))
        for index, image in enumerate(self.images):
            # rgb
            for channel in range(3):
                Z[:, index, channel] = self.get_pixel(image.data, sample_space)
        return Z

    def get_radiance(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        self.radiance = np.zeros((255, 3))
        for channel in range(3):
            g, lE = self.gsolve(self.Z[:, :, channel], channel)
            self.radiance[:, channel] = g[:, 0]

        return self.radiance


    def get_Ab(self, Z, n=256):
        k = 0
        A = np.zeros((Z.shape[0] * Z.shape[1] + n + 1, n + Z.shape[0]))
        b = np.zeros((A.shape[0], 1))
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                Z_ij = int(round(Z[i, j]))
                w_ij = self.weigth_function(Z_ij + 1)

                A[k, Z_ij] = w_ij
                A[k, n + i ] = -w_ij

                w_ij = self.weigth_function(int(Z[i, j]) + 1)
                b[k, 0] = w_ij * self.B[j]
                k += 1

        A[k, 128] = 1
        k += 1

        for i in range(0, n - 3):
            A[k, i] = self.lambda_constant * self.weigth_function(i + 2 )
            A[k, i + 1] = -2 * self.lambda_constant * self.weigth_function(i+2)# + 1)
            A[k, i + 2] = self.lambda_constant * self.weigth_function(i+2)# + 1)
            k += 1
        return A, b, n

    def gsolve(self, Z, index):
        """
        [TODO:summary]

        [TODO:description]
        """
#        n = 256
        A, b, n  = self.get_Ab(Z)

#        exitcode = 0
 #       a_matlab_before = scipy.io.loadmat("./files/matlab_a_before_second_loop {}.mat".format(index + 1))["A"]
  #      b_matlab = scipy.io.loadmat("./files/matlab_b {}.mat".format(index + 1))["b"]
    

        """
        Big matlab hack
        """
        scipy.io.savemat('./files/Ab.mat', dict(A=A, b=b))

        LOAD_COMMAND = "load('./files/Ab.mat');"
        STORE_COMMAND = "save(['./files/matlab_x.mat'],'x');"
        COMMAND = LOAD_COMMAND + "x=A\\b; " + STORE_COMMAND + "exit;"

        x_matlab = scipy.io.loadmat("./files/matlab_x {}.mat".format(index + 1))["x"]
        os.system("/Applications/MATLAB_R2019a.app/bin/matlab -nodisplay -r \"{}\"".format(COMMAND))

        print(COMMAND)

        x = scipy.io.loadmat("./files/matlab_x.mat")["x"]
   
        """
        Big matlab hack is over
        """

        g = x[1:n]
        lE = x[n + 1:x.shape[0]]
        return g, lE

    def look_up_pixel(self, radiance, image):
        out_image = np.zeros((image.shape))
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                out_image[i, j] = radiance[int(image[i, j]) - 1]
        return out_image

    '''
	Equation 6 from the paper
	'''
    def get_radiance_log(self, radiance):
        x = np.ones(self.images[0].data.shape)
        y = np.zeros(self.images[0].data.shape)

        for index, i in enumerate(self.images):
            g = i.data.copy()
            for rgb in range(3):
                g[:, :, rgb] = self.look_up_pixel(radiance[:, rgb], g[:, :, rgb])
            g -= self.B[index]
            f = np.vectorize(self.weigth_function)
            wi = f(g.copy())
            x += wi * g
            y += wi
        rad = (x / y)
        return rad  # (x/y).clip(0, 255)
