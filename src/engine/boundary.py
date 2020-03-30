from nptyping import Array

class Boundary:
    """
    This class describes the boundary conditions
    """

    def __init__(self, u0=None):
        #self.data = None
        self.u0 = u0

    def set_u0(self, data):
        print("got set")
        self.u0 = data

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
        return data.clip(0, 1)

    def diriclet(self, data: Array[float, float] = None, mask=None):
        if(mask is None):
            data[:, 0] = self.u0[:, 1]
            data[:, -1] = self.u0[:, -2]
            data[0, :] =  self.u0[1, :]
            data[-1, :] =  self.u0[-2, :]
        else:
            data[~mask.astype(bool)] = self.u0[~mask.astype(bool)] 
        return data.clip(0, 1)
