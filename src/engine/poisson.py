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

        self.mode = self.IMPLICIT
        #self.data = None
        pass

    def get_laplace(self, data: Array[float, float] = None) -> Array:
        """
        Gets the laplace

        Parameters
        ----------
        data : ndarray
            The data to get the laplace from
        """
        if data is None:
#            raise Exception("Data not set")
            data = self.data
        laplace = data[0:-2, 1:-1] \
                  + data[2:, 1:-1] \
                  + data[1:-1, 0:-2] \
                  + data[1:-1, 2:] \
                  - 4 * data[1:-1, 1:-1]
        return laplace

    def explicit(self, data, h):
        alpha = 0.25
        return (alpha * self.get_laplace(data) - h(data)[1:-1, 1:-1])

    def implicit(self, data, h):
        # Systemmatrisen
        j = self.data.shape[1]
        i = self.data.shape[0]

        """
        wait, how do we set a h in this ? 

        """
        # we need 2 diagonals for i and j 
        upperdiag = np.concatenate(([0, 0], -self.alpha * np.ones(j - 2)))
        upperdiag1 = np.concatenate(([0, 0], -self.alpha * np.ones(i - 2)))

        centerdiag = np.concatenate(([1], (1 + 4 * self.alpha) * np.ones(j - 2),
                                     [1]))

        # we need 2 diagonals for i and j
        lowerdiag = np.concatenate((-self.alpha * np.ones(j - 2), [0, 0]))
        lowerdiag1 = np.concatenate((-self.alpha * np.ones(i - 2), [0, 0]))

        diags = np.array([upperdiag, upperdiag1, centerdiag, lowerdiag, lowerdiag1])
        A = spdiags(diags, [2, 1, 0, -1, -2], j, j).tocsc()

     #   print(self.data.shape)
    #    print(h(self.data).shape)
        return spsolve(A, self.data[:, :]) - h(self.data)

    def solve(self, data, h=lambda x: 0):
        if(self.mode == self.EXPLICIT):
            data[1:-1, 1:-1] += self.explicit(data, h)
        elif(self.mode == self.IMPLICIT):
            data[:, :] = self.implicit(data, h)
        else:
            raise Exception("Not supported")
        return data










