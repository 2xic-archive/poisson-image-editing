from nptyping import Array


class poisson:
    """
    This class describes the abstracts part of the poisson equation
    """

    def __init__(self):
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
            raise Exception("Data not set")
#            data = self.data
        laplace = data[0:-2, 1:-1] \
                  + data[2:, 1:-1] \
                  + data[1:-1, 0:-2] \
                  + data[1:-1, 2:] \
                  - 4 * data[1:-1, 1:-1]
        return laplace
