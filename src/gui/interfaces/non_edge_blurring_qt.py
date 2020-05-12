from backend import non_edge_blurring
from gui.general_window import *


class non_edge_blurring_window(general_window):
    """
    This class describes a non edge blurring window.
    """

    def __init__(self, parent=None):
        general_window.__init__(self, load_before=lambda : self.load_before_content())
        self.method = non_edge_blurring.NonEdgeBlur(self.image)

    def load_before_content(self):
        """
        Adds the option for data attachment

        This element is added after the image
        """
        self.contrast_k_text = self.add_label("Contrast K variable")
        self.update_geometry(self.pixmap.width(), 30)

        self.k_value = self.add_slider("How much should we blur?", lambda x: QTimer.singleShot(100, lambda:self.update_K()), value=10)
        self.update_geometry(self.pixmap.width(), 30)

    def update_K(self):
        """
        Update the k value for the method
        """
        self.method.K = self.k_value.value()