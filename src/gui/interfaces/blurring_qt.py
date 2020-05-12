from backend import blurring
from gui.general_window import *


class blur_window(general_window):
    """
    This class describes a blur window.
    """

    def __init__(self, parent=None):
        general_window.__init__(self, load_before=lambda: self.load_before_content())
        self.method = blurring.Blur(self.image)

    def load_before_content(self):
        """
        Adds the option for data attachment

        This element is added after the image
        """
        self.data_attachment_label = self.add_label("Data attachment")
        self.update_geometry(self.pixmap.height(), 30, x=10)

        self.lambda_size = self.add_slider("How strong should the blur be?", lambda x: QTimer.singleShot(100, lambda:self.update_lambda()))
        self.update_geometry(self.pixmap.height(), 30)

        """
        Turn off or on the colors
        """
        self.color_checkbox = self.add_checkbox('Use color?', action=self.update_image_color)
        self.update_geometry(self.pixmap.width(), 30)

    def update_image_color(self, _):
        """
        Allows you to change the image from grayscale to color
        """
        self.method.change_color_state()
        self.update_image_label()
        self.reset_image()

    def update_lambda(self):
        """
        Update the lambda constant
        """
        self.method.set_lambda_size(self.lambda_size.value() / self.lambda_size.maximum())
        