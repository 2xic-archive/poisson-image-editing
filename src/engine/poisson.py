from nptyping import Array
import numpy as np
from scipy.sparse import spdiags
from scipy.sparse.linalg import spsolve

class poisson:
    """
    This class describes the abstracts part of the poisson equation
    """

    def __init__(self):
        self.EXPLICIT = 0
        self.IMPLICIT = 1 

#        self.mode_poisson = self.EXPLICIT
        self.mode_poisson = self.IMPLICIT
        self.alpha = 0.25

    def get_laplace_explicit(self, data: Array[float, float] = None) -> Array:
        """
        Gets the laplace

        Parameters
        ----------
        data : ndarray
            The data to get the laplace from
        """
        if data is None:
            data = self.data
        laplace = data[0:-2, 1:-1] \
                  + data[2:, 1:-1] \
                  + data[1:-1, 0:-2] \
                  + data[1:-1, 2:] \
                  - 4 * data[1:-1, 1:-1]
        return laplace * self.alpha


    def get_laplace_implicit(self, data):#, h):
        # Systemmatrisen
        j = data.shape[1]
        i = data.shape[0]

        j = i

        # we need 2 diagonals for i and j 
        upperdiag = np.concatenate(([0, 0], -self.alpha * np.ones(j - 2)))
        upperdiag1 = np.concatenate(([0, 0], -self.alpha * np.ones(j - 2)))

        centerdiag = np.concatenate(([1], (1 + 4 * self.alpha) * np.ones(j - 2),
                                     [1]))


        # we need 2 diagonals for i and j
        lowerdiag = np.concatenate((-self.alpha * np.ones(j - 2), [0, 0]))
        lowerdiag1 = np.concatenate((-self.alpha * np.ones(j - 2), [0, 0]))



        diags = np.array([upperdiag, upperdiag1, centerdiag, lowerdiag, lowerdiag1])

        A = spdiags(diags, [2, 1, 0, -1, -2], i, j).tocsc()

        return spsolve(A, data[:, :])

        # - h(self.data)

    def common_shape(self, data):
        if self.mode_poisson == self.EXPLICIT:
            return data[1:-1, 1:-1]
        elif self.mode_poisson == self.IMPLICIT:
            return data
        else:
            raise Exception(" not supported")

    def get_laplace(self, data):
        if self.mode_poisson == self.EXPLICIT:
            return self.get_laplace_explicit(data)
        elif self.mode_poisson == self.IMPLICIT:
            return self.get_laplace_implicit(data)
        else:
            raise Exception(" not supported")

    def solve(self, data, operator, h=lambda x=None, i=None: 0):
        if self.mode_poisson == self.EXPLICIT:
            if(len(data.shape) == 3):
                for i in range(3):#data.shape[-1]):
                    data[1:-1, 1:-1, i] += operator(i) - h(i=i)
            else:
                data[1:-1, 1:-1] += operator() - h(data)
        elif self.mode_poisson == self.IMPLICIT:
            if(len(data.shape) == 3):
                for i in range(3):#data.shape[-1]):
                    data[:, :, i] = operator(i=i) - h(i=i)
            else:
                data[:, :] = operator() - h(data)
        else:
            raise Exception("Not supported")
        return data






