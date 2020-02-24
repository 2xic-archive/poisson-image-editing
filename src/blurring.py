import loader
class blur(loader.ImageLoader):
    def __init__(self, path):
        loader.ImageLoader.__init__(self, path)
        
        self.alpha = 0.4
        
    def eksplisitt(self):
        """
        [TODO:summary]

        [TODO:description]
        """
        laplace = self.data[0:-2, 1:-1] \
                + self.data[2:, 1:-1] \
                + self.data[1:-1, 0:-2] \
                + self.data[1:-1, 2:]   \
                - 4 * self.data[1:-1, 1:-1]
        self.data[1:-1, 1:-1] += self.alpha * laplace

    def fit(self,epochs):
        """
        [TODO:summary]

        [TODO:description]

        Parameters
        ----------
        epochs : [TODO:type]
            [TODO:description]
        """
        for i in range(epochs):
            self.eksplisitt()
        return self.data
