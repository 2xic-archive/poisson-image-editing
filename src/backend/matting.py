import os
import image_handler
import poisson


def get_path(file):
    dir_path = os.path.dirname(os.path.realpath(file)) + "/"
    return dir_path


class matting(image_handler.ImageHandler, poisson.poisson):
    def __init__(self, target_path="./files/test_images/target.png", source_path="./files/test_images/source.png",
                 color=True):
        target_path = get_path(__file__) + "../files/test_images/target.png"
        source_path = get_path(__file__) + "../files/test_images/source.png"

        image_handler.ImageHandler.__init__(self, target_path, color)
        poisson.poisson.__init__(self)
        self.alpha = 0.2

        # the bird
        self.source = image_handler.ImageHandler(source_path, color)
        self.target = self.data.copy()

        # NOTE : If this is wide the effect will go badly (I tried without having this set and you
        # get a ugly border)
        # NOTE2 : I realized that it is because the photo contained a black border
        # TODO : Make it possible to set/define these values in GUI
        self.area = (
            (200, 50),
            (250, 130),
        )
        print(self.area)

    def get_area(self):
        pass

    def iteration(self):
        """
		[TODO:summary]

		[TODO:description]
		"""
        crop_area = lambda x: x[self.area[0][0]:self.area[1][0],
                              self.area[0][1]:self.area[1][1]]

        target_laplace = self.get_laplace(crop_area(self.target))
        source_laplace = self.get_laplace(crop_area(self.source.data))
        working_area = crop_area(self.data)
        working_area[1:-1, 1:-1] += (target_laplace - source_laplace) * self.alpha

        # TODO : make this "nice"
        self.data[self.area[0][0]:self.area[1][0],
        self.area[0][1]:self.area[1][1]] = working_area.clip(0, 1)

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
