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

        self.mode_poisson = self.EXPLICIT
#        self.mode_poisson = self.IMPLICIT
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
#            raise Exception("Data not set")
            data = self.data
        laplace = data[0:-2, 1:-1] \
                  + data[2:, 1:-1] \
                  + data[1:-1, 0:-2] \
                  + data[1:-1, 2:] \
                  - 4 * data[1:-1, 1:-1]
        return laplace * self.alpha

#    def explicit(self, data, h):
#        return (self.alpha * self.get_laplace_explicit(data) - h(data)[1:-1, 1:-1])
#        return (self.alpha * self.get_laplace_explicit(data) - h(data)[1:-1, 1:-1])


    def get_laplace_implicit(self, data):#, h):
        # Systemmatrisen
        j = data.shape[1]
        i = data.shape[0]

        j = i
     #   i = max(j, i)
    #    j = i

        # we need 2 diagonals for i and j 
        upperdiag = np.concatenate(([0, 0], -self.alpha * np.ones(j - 2)))
        upperdiag1 = np.concatenate(([0, 0], -self.alpha * np.ones(j - 2)))

        centerdiag = np.concatenate(([1], (1 + 4 * self.alpha) * np.ones(j - 2),
                                     [1]))

  #      print(upperdiag1)
 #       print(centerdiag)
#        exit(0)

        # we need 2 diagonals for i and j
        lowerdiag = np.concatenate((-self.alpha * np.ones(j - 2), [0, 0]))
        lowerdiag1 = np.concatenate((-self.alpha * np.ones(j - 2), [0, 0]))



        diags = np.array([upperdiag, upperdiag1, centerdiag, lowerdiag, lowerdiag1])

        print(upperdiag.shape)
        print(upperdiag1.shape)
        print(centerdiag.shape)
        print(lowerdiag.shape)
        print(lowerdiag1.shape)
        print(diags.shape)
        A = spdiags(diags, [2, 1, 0, -1, -2], i, j).tocsc()
    #    print(spsolve(A, data[:, :]))
     #   exit(0)

     #   print(self.data.shape)
    #    print(h(self.data).shape)
 #       print(A.shape)
  #      print(data.shape)
        return spsolve(A, data[:, :])

        # - h(self.data)

    def common_shape(self, data):
        if(self.mode_poisson == self.EXPLICIT):
            return data[1:-1, 1:-1]
        elif(self.mode_poisson == self.IMPLICIT):
            return data
        else:
            raise Exception(" not supported")

    def get_laplace(self, data):
        if(self.mode_poisson == self.EXPLICIT):
            return self.get_laplace_explicit(data)
        elif(self.mode_poisson == self.IMPLICIT):
            return self.get_laplace_implicit(data)
        else:
            raise Exception(" not supported")

    def solve(self, data, operator, h=lambda x: 0):
        if(self.mode_poisson == self.EXPLICIT):
            # so a problem is how do you decalre if you have used the laplace or not ? 
            data[1:-1, 1:-1] += operator() - h(data)
        elif(self.mode_poisson == self.IMPLICIT):
            data[:, :] = operator() - h(data)
        else:
            raise Exception("Not supported")
        return data






