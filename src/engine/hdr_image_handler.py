import numpy as np
from engine import image_handler
from itertools import combinations
import scipy.io

"""
TODO : I now see that multiple solutions to the problem is mentioned in the project description	*awkward* will try them out
"""


# NOTE : THIS DOES NOT SEEM TO WORK 
# https://stackoverflow.com/questions/33559946/numpy-vs-mldivide-matlab-operator
def matlab_mdivide(A, b):
    num_vars = A.shape[1]
    rank = np.linalg.matrix_rank(A)
    sol = None
 #   return np.linalg.lstsq(A, b)[-1]
    if rank == num_vars:
#        print("just return")
        sol = np.linalg.lstsq(A, b)[-1]  # not under-determined
    else:
        sol = np.zeros((num_vars, 1))
        print("??")
        print(len(combinations(range(num_vars), rank)))
        for nz in combinations(range(num_vars), rank):  # the variables not set to zero
            try:
                sol[nz, :] = np.asarray(np.linalg.solve(A[:, nz], b))
                print(sol)
            except np.linalg.LinAlgError:
                pass  # picked bad variables, can't solve
    #	print(sol.shape, num_vars)
    return sol


# as defined in equation 3
def weigth_function(intensity: float):
    """
	[TODO:summary]

	[TODO:description]
	"""
    if intensity <= 128:
        return intensity
    return 255 - intensity


class hdr_handler:
    def __init__(self):
        self.images = [
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00064.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00128.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00256.png'),
            image_handler.ImageHandler('../hdr-bilder/Adjuster/Adjuster_00512.png')
        ]
        for i in self.images:
            i.resize(scale=4)

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
        self.l = 100  # is lamdba, the constant that determines the amount of smoothness

        self.Z = scipy.io.loadmat("./files/Z.mat")["Z"]
        #self.Z = scipy.io.loadmat("./files/Z.mat")["Z"]
#        print(self.sample().shape)
#        scipy.io.savemat('./files/Z.mat', dict(Z=self.sample()))
#        exit(0)

    # self.sample()

    def get_pixel(self, image, sample):
        """
        [TODO:summary]

        [TODO:description]
        """
        results = np.zeros(sample.shape)
        # print(sample.shape)
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
                #	print(sample_space.shape)
                #	print(image.data.shape)
                #	print(Z.shape)
                #	print(self.get_pixel(image.data, sample_space).shape)
                Z[:, index, channel] = self.get_pixel(image.data, sample_space)  # .reshape()
#        import scipy.io
#        scipy.io.savemat('./files/Z.mat', dict(Z=Z))
#        exit(0)
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

    def gsolve(self, Z, index):
        """
        [TODO:summary]

        [TODO:description]
        """
        n = 256
        A = np.zeros((Z.shape[0] * Z.shape[1] + n + 1, n + Z.shape[0]))
        b = np.zeros((A.shape[0], 1))

        k = 1
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                Z_ij = int(Z[i, j])
                w_ij = weigth_function(Z_ij + 1)
                A[k, Z_ij + 1] = w_ij
                A[k, n + 1] = -w_ij

                b[k, 0] = w_ij * self.B[j]
                k += 1

        A[k, 129] = 1
        k += 1
        for i in range(0, n - 2):
            A[k, i] = self.l * weigth_function(i + 1)
            A[k, i + 1] = -2 * self.l * weigth_function(i + 1)
            A[k, i + 2] = self.l * weigth_function(i + 1)
            k += 1

        A[k, 129] = 0
        from scipy.optimize import nnls
        from scipy.optimize import leastsq


        LOAD_COMMAND = "load('./files/Ab.mat');"
        #LOAD_B_COMMAND = "load('b.mat');"
        scipy.io.savemat('./files/Ab.mat', dict(A=A, b=b))
        STORE_COMMAND = "save(['./files/matlab_x.mat'],'x');"

        COMMAND = LOAD_COMMAND + "x=A\\b; " + STORE_COMMAND + "exit;"
        import os
        os.system("/Applications/MATLAB_R2019a.app/bin/matlab -nodisplay -r \"{}\"".format(COMMAND))
        print(COMMAND)
        x = scipy.io.loadmat("./files/matlab_x.mat")["x"]
#        print(x)
 #       exit(0)

        '''
        print(A.shape)
        print(b.shape)

        a_matlab = scipy.io.loadmat("./files/matlab_a {}.mat".format(index + 1))["A"]
        b_matlab = scipy.io.loadmat("./files/matlab_b {}.mat".format(index + 1))["b"]
        x_matlab = scipy.io.loadmat("./files/matlab_x {}.mat".format(index + 1))["x"]
        print((b - b_matlab).sum())
        print((A - a_matlab).sum())
        '''
 #       print(A.shape)
#        print(b.shape)
 #       x = (nnls(A, b[:, 0]))[0]
  #      print(leastsq(A, b))
   #     x = leastsq(A, b[:, 0])#[0]
     #   x = matlab_mdivide(A, b[:, 0])
      #  print("lstsq", (x_matlab - x).sum())
       # exit(0)

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
            f = np.vectorize(weigth_function)
            wi = f(g.copy())
            x += wi * g
            y += wi
        #		print(np.max(x/y))
        rad = (x / y)
        return rad  # (x/y).clip(0, 255)
