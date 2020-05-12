import re

from PyQt5.QtCore import Qt

from backend import matting
from gui.general_window import *
from gui.general import *

import numpy as np

class matting_window(general_window):
    """
    This class describes a matting window.
    """

    def __init__(self, parent=None):
        general_window.__init__(self, lambda x: Image.fromarray((x * 255).astype(np.uint8)),
                                load_before=lambda: self.load_extra_now())
        self.method = matting.Matting()

    def get_int(self, field) -> int:
        """
        Makes sure the pixel format is correct

        Parameters
        ----------
        field : str
            the text to extract the number from

        Returns
        -------
        int
            the int from the text
        """
        response = re.findall(r'\d+', field)
        if (len(response) == 0):
            return -1
        return int(response[0])

    def load_extra_now(self):
        """
        Showing the image
        """
        self.setAcceptDrops(True)
        self.label_, self.pixmap_ = self.add_image_draggable(self.method.source.data, (
            lambda x: self.pixmap_converter(x)) if not self.pixmap_converter is None else (
            lambda x: Image.fromarray(255 * x)), self)

        self.boundary_box, self.boundary_group_iamge_end = self.add_input_group("Start coordinates", [
            "x", "y"
        ],
                                                                                [
                                                                                    lambda x: QTimer.singleShot(100,
                                                                                                                lambda: self.update_image_size()),
                                                                                    lambda x: QTimer.singleShot(100,
                                                                                                                lambda: self.update_image_size())
                                                                                ])
        self.update_geometry(self.boundary_box.width(), 90, x=10)

        self.boundary_box_max, self.boundary_group_iamge = self.add_input_group("End coordinates", [
            "x1", "y1"
        ], [
                                                                                    lambda x: QTimer.singleShot(100,
                                                                                                                lambda: self.update_image_size()),
                                                                                    lambda x: QTimer.singleShot(100,
                                                                                                                lambda: self.update_image_size())
                                                                                ])
        self.update_geometry(self.boundary_box_max.width(), 90, x=10 + self.boundary_box.width(), y=-42)
        self.update_image_size()

    def update_image_size(self):
        """
        Update the image size based on the input size
        """
        x0, y0, x1, y1 = list(
            map(lambda x: self.get_int(x.text()), self.boundary_group_iamge_end + self.boundary_group_iamge))
        if x0 == -1:
            x0 = 0
        if y0 == -1:
            y0 = 0
        if x1 == -1:
            x1 = self.method.source.data.shape[1]
        if y1 == -1:
            y1 = self.method.source.data.shape[0]
        if x0 < x1 and y0 < y1:
            self.area = [[x0, x1], [y0, y1]]
            self.label_.setPixmap(
                pil2pixmap(Image.fromarray((255 * self.method.source.data[y0:y1, x0:x1]).astype(np.uint8))))

    def prepare(self):
        """
        Prepare the method before run
        """
        self.method.working_area = self.area
        self.method.padding = [self.label_.pos().x(), self.label_.pos().y()]
        self.label_.setVisible(False)

    def undo(self):
        self.label_.setVisible(True)

    def dragEnterEvent(self, e):
        """
        Drag event handler for the source image

        Parameters
        ----------
        e : QDragEnterEvent
            The drag event
        """
        e.accept()

    def dropEvent(self, e):
        """
        Drop event handler for the source image

        Parameters
        ----------
        e : QDropEvent
            The drop event
        """
        position = e.pos()
        self.label_.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()
