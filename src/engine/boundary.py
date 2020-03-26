from nptyping import Array

class Boundary:
    """
    This class describes the boundary conditions
    """

    def __init__(self):
        #self.data = None
        pass

    def neumann(self, data: Array[float, float] = None):
        """
        Preform a neumann boundary

        Parameters
        ----------
        data : ndarray
            The data to preform the boundary on
        """
        if data is None:
#            raise Exception("Data not set")
            data = self.data
        # Neumann randbetingelse
        data[:, 0] = data[:, 1]
        data[:, -1] = data[:, -2]
        data[0, :] = data[1, :]
        data[-1, :] = data[-2, :]
        return data
