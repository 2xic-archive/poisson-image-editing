class Boundary:
    """
    This class describes the boundary conditions
    """
    def __init__(self):
        pass

    def neumann(self, data=None):
        """
        Preform a neumann boundary

        Parameters
        ----------
        data : ndarray
            The data to preform the boundary on
        """
        if data is None:
            data = self.data
        data[:, 0] = data[:, 1]      # Neumann randbetingelse
        data[:, -1] = data[:, -2]    #
        data[0, :] = data[1, :]      #
        data[-1, :] = data[-2 , :]   #
        return data