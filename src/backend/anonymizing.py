from __future__ import annotations

from nptyping import Array

from backend import blurring
from engine import boundary
from engine import image_handler, poisson


def get_mask(path: str) -> list:
    """
    Get a(ll) the mask(s) boxes to blur some face(s)


    Parameters
    ----------
    path : str
        path to the image file to anonymize

    Returns
    -------
    list
        a list with bounding boxes of (x, x1, y, y1) for the faces
    """
    from cv2 import CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY
    face_cascade = CascadeClassifier(
        './files/haarcascade_frontalface_default.xml')
    img = imread(path)
    gray = cvtColor(img, COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    results = []
    for (x, y, w, h) in faces:
        results.append([x, x + w, y, y + h])
    return results


class Anonymous(
    image_handler.ImageHandler,
    poisson.Poisson,
    boundary.Boundary):
    """
    This class describes a anonymous image.

    This contains all the functions needed to anonymize a image over multiple iterations

    """
    mask: list

    def __init__(self, path: str, color: bool = True):
        """
        Constructs a new instance of the Anonymous object.

        Parameters
        ----------
        path : str
            path to a image file
        color : bool
            if the image should be shown with colors
        """
        image_handler.ImageHandler.__init__(self, path, color)
        poisson.Poisson.__init__(self)
        boundary.Boundary.__init__(self)

        self.mask = get_mask(path)

    def iteration(self) -> Array:
        """
        Does one iteration of the method.

        Returns
        -------
        ndarray
            returns the new computed image
        """
        blur = blurring.Blur(None)
        for mask in self.mask:
            blur.set_data(self.data.copy()[mask[0]:mask[1], mask[2]:mask[3]])
            blur.set_boundary("dirichlet")
            self.data[mask[0]:mask[1], mask[2]:mask[3]] = blur.iteration()
        return self.data

    def fit(self, epochs: int) -> Anonymous:
        """
        Makes multiple iterations of the method

        Calls iteration as many times as specified in by the parameter epochs

        Parameters
        ----------
        epochs : int
            The iteration count

        Returns
        -------
        anonymous
            returns self
        """
        for _ in range(epochs):
            self.iteration()
        return self
