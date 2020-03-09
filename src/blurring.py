import loader
import numpy as np
from PIL import Image
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
        return self#.data

    def save(self, name):
        from PIL import Image
        im = Image.fromarray(np.uint8(self.data))#Image.fromarray(self.data, 'RGB')
        im.save(name)#"your_file.jpeg")
        return name