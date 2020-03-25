import os
from engine import image_handler, poisson
from backend import blurring

from gui.general import get_path
from engine.image_handler import ImageHandler


def get_mask(path: str) -> list:
    """
    Get the mask to blur a face


    Parameters
    ----------
    path : str
        path to the image file to anonymize
    """
    from cv2 import CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY
    face_cascade = CascadeClassifier('./files/haarcascade_frontalface_default.xml')
    img = imread(path)
    gray = cvtColor(img, COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    results = []
    for (x, y, w, h) in faces:
        results.append([x, x + w, y, y + h])
    return results


class anonymous(image_handler.ImageHandler, poisson.poisson):
    """
    This class describes a anymous image.

    This contains all the functions needed to anonymize a image over multiple iterations

    Parameters
    ----------
    path : str
        path to a image file
    color : bool
        if the image should be shown with colors
    """
    mask: list

    def __init__(self, path: str, color: bool = False):
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.poisson.__init__(self)
        self.alpha: float = 0.1
        self.mask = get_mask(path)
        self.u0 = self.data.copy()

    def iteration(self) -> None:
        """
        Does one iteration of the method.

        """
        blur = blurring.blur(None)
        for mask in self.mask:
            blur.set_data(self.data.copy()[mask[0]:mask[1], mask[2]:mask[3]])
            self.data[mask[0]:mask[1], mask[2]:mask[3]] = blur.iteration()

    def fit(self, epochs: int):
        """
        Makes multiple iterations of the method

        Calls iteration as many times as spesifed in by the parameter epochs

        Parameters
        ----------
        epochs : int
            The iteration count
        """
        for _ in range(epochs):
            self.iteration()
        return self
