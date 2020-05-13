from __future__ import annotations

from nptyping import Array

from engine import boundary
from engine import image_handler
from engine import poisson


class Matting(image_handler.ImageHandler, poisson.Poisson, boundary.Boundary):
    """
    This class describes a matting image.

    This contains all the functions needed to merge a image over another image over multiple iterations
    """

    def __init__(self, target_path="./files/test_images/target.png", source_path="./files/test_images/source_v2.png",
                 area=[[10, 65],
                       [10, 65]],
                 padding=[50, 250],
                 color=True):
        """
        Constructs a new instance of the Matting object.

        Parameters
        ----------
        target_path : str
            Path to the target image
        source_path : str
            Path to a source image to add on the target
        area : list
            List with [(x0, x1), (y0, y1)], sets the working area in the source image
        padding : list
            List with (x, y) to put the working area at the correct location in the target image
        color : bool
            If the image should be shown with colors
        """
        image_handler.ImageHandler.__init__(self, target_path, color)
        boundary.Boundary.__init__(self)
        poisson.Poisson.__init__(self)

        self.source = image_handler.ImageHandler(source_path, color)
        self.target = self.data.copy()

        self.working_area = area
        self.padding = padding

    @property
    def working_area(self) -> list:
        """
        Return the working area

        Returns
        -------
        list
            The working area [(x0, x1), (y0, y1)]
        """
        return self._area

    @working_area.setter
    def working_area(self, location):
        """
        Setter for the working area

        This is a setter that makes sure that the data that is set is valid.

        Parameters
        ----------
        location : int
            The location of the working area for the images
        """
        if len(location) != 2:
            raise ValueError("You specify the area as a 2d tuple ((x0, x1), (y0, y1))")

        x0, x1 = location[0]
        if x0 is None:
            x0 = 0
        if x1 is None:
            x1 = self.source.data.shape[1]

        if x0 < 0 or self.source.data.shape[1] < x1:
            raise ValueError("x range is ({}, {})".format(0, self.source.data.shape[1]))

        y0, y1 = location[1]
        if y0 is None:
            y0 = 0
        if y1 is None:
            y1 = self.source.data.shape[0]

        if not y0 < y1:
            raise ValueError("y0 should be less than y1")
        if y0 < 0 or self.source.data.shape[0] < y1:
            raise ValueError("x range is ({}, {})".format(0, self.source.data.shape[0]))
        self._area = [(x0, x1), (y0, y1)]

    def preview_box(self, x, y, x1, y1) -> Array:
        """
        Preview the crop box

        Parameters
        ----------
        x : int
            The x0 location
        y : int
            The y0 location
        x1 : int
            The x1 location
        y1 : int
            The y1 location

        Returns
        -------
        ndarray
            The cropbox
        """
        self.working_area = ((x, x + self.source.data.shape[1]), (y, y + self.source.data.shape[0]))

        box = self.target.copy()
        x0, x1 = self.working_area[0][0], self.working_area[0][1]
        y0, y1 = self.working_area[1][0], self.working_area[1][1]
        box[y0:y1,
        x0:x1:] = 255
        return box

    def reset_full(self) -> None:
        """
        Reset the image source and target
        """
        self.source.reset()
        self.reset()

    def crop(self, in_data, with_padding=True) -> Array:
        """
        Crops the image

        Parameters
        ----------
        in_data : ndarray
            The data to crop
        with_padding : bool
            If you want to add the padding location to the workig_area (used on the target image)

        Returns
        -------
        ndarray
            The new cropped image array
        """
        if with_padding:
            return self.convert_single(in_data[self.working_area[1][0] + self.padding[1]:self.working_area[1][1] + self.padding[1],
                   self.working_area[0][0] + self.padding[0]:self.working_area[0][1] + self.padding[0]])
        return self.convert_single(in_data[self.working_area[1][0]:self.working_area[1][1],
               self.working_area[0][0]:self.working_area[0][1]])

    def convert_single(self, data):
        if len(data.shape) == 3:
            return data[:, :, :]
        return data

    def apply(self, in_data):
        """
        Apply the data to the image

        Sets the new data based on the padding and area size

        Parameters
        ----------
        in_data : ndarray
            The data to set onto the image data
        """
        if len(self.data.shape) == 3:
            for channel in range(min(self.data.shape[-1], in_data.shape[-1])):
                self.data[self.working_area[1][0] + self.padding[1]:self.working_area[1][1] + self.padding[1],
                self.working_area[0][0] + self.padding[0]:self.working_area[0][1] + self.padding[0], channel] = in_data[:, :, channel]
        else:
            self.data[self.working_area[1][0] + self.padding[1]:self.working_area[1][1] + self.padding[1],
                self.working_area[0][0] + self.padding[0]:self.working_area[0][1] + self.padding[0]] = in_data[:, :]

    def iteration(self) -> Array:
        """
        Does one iteration of the method.

        Returns
        -------
        ndarray
            The new image array
        """
        working_area = self.crop(self.data)
        solved_working_area = self.solve(working_area, self.operator, self.h,
                                         apply_boundary=False)
        self.apply(solved_working_area)
        return self.data

    def operator(self, i=None) -> Array:
        """
        Solves the "u" part of the Poisson equation

        Parameters
        ----------
        i : int
            The channel to "work" on

        Returns
        -------
        ndarray
            The u value
        """
        working_area = self.crop(self.data)
        if i is None:            
            return self.get_laplace(working_area[:, :])
        else:
            return self.get_laplace(working_area[:, :, i])

    def h(self, i=None) -> Array:
        """
        Solves the "h" part of the Poisson equation

        Parameters
        ----------
        i : int
            The channel to "work" on

        Returns
        -------
        ndarray
            The h value
        """
        working_area_source = self.crop(self.source.data, False)
        if i is None:
            return self.get_laplace((working_area_source)[:, :])
        else:
            return self.get_laplace((working_area_source)[:, :, i])

    def bad_fit(self):
        """
        Will directly paste the source image onto the target image
        """
        working_area_source = self.crop(self.source.data, with_padding=False)
        self.apply(working_area_source)

    def fit(self, epochs=1) -> matting:
        """
        Makes multiple iterations of the method

        Calls iteration as many times as specified in by the parameter epochs

        Parameters
        ----------
        epochs : int
            The iteration count

        Returns
        -------
        Matting
            Returns self
        """
        for i in range(epochs):
            self.iteration()
        return self
