import image_handler
import numpy as np
import poisson


class contrast(image_handler.ImageHandler, poisson.poisson):
    """

    """
    def __init__(self, path, color=False):
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        self.alpha = 0.1
        self.k = 1
        self.u0 = np.copy(self.data)

    def iteration(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        laplace = self.get_laplace()
        #    TODO: check if this is correct. 
        self.data[1:-1, 1:-1] += (self.u0[1:-1, 1:-1] - (self.k * laplace)) * self.alpha
        # ((laplace) - (self.k * self.u0[1:-1, 1:-1])) * self.alpha <- guess i had it backwards?
        self.data = self.data.clip(0, 1)

        """
        TODO : Implement Neumann
        """

    def fit(self, epochs=1):
        """
        [TODO:summary]

        [TODO:description]

        Parameters
        ----------
        epochs : int
            The iteration count
        """
        for i in range(epochs):
            self.iteration()
        return self
