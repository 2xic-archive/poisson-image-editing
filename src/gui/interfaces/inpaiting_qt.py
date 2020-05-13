from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from nptyping import Array

from backend import inpaiting
from extra.median_filter import median_filter
from gui.general_window import *
from gui.general import *
import numpy as np

class inpait_window(general_window):
    """
    This class describes an inpaint window.
    """

    def __init__(self, parent=None):
        general_window.__init__(self, load_extra=lambda: self.load_after(),
                                load_before=lambda: self.load_before_content())
        self.method = inpaiting.Inpaint(self.image)
        self.input_image = self.method.get_data().copy()

    def load_before_content(self):
        """
        Adds the option to remove information
        """
        self.noise_label = self.add_label("Remove information")
        self.update_geometry(self.pixmap.height(), 30)

        self.noise_slider = self.add_slider("How much information to remove?", self.epochs_change, max_value=10)
        self.update_geometry(self.pixmap.height(), 30)

        self.noise_button = self.add_button("Remove",
                                            lambda x: QTimer.singleShot(100, lambda: self.update_image_noise()))
        self.update_geometry(self.pixmap.height(), 30)
        """
        Turn off or on the colors
        """
        self.color_checkbox = self.add_checkbox('Use color?', action=self.update_image_color)
        self.update_geometry(self.pixmap.width(), 30)

    def update_image_color(self, _):
        """
        Update the image if the color state is changed
        """
        self.method.change_color_state()
        self.update_image_label()
        self.reset_image()

    def load_after(self):
        """
        Generate the extra row
        """
        _, self.height = self.position()
        self.PADDING = self.pixmap.width() + 30

        self.extra_button = self.add_button("Extra", lambda x: QTimer.singleShot(100, lambda: self.show_extra()))
        self.update_geometry(self.pixmap.width(), 30)

        self.extra_label, self.extra_pixmap = self.add_image(self.method.data, (
            lambda x: self.pixmap_converter(x)) if not self.pixmap_converter is None else (
            lambda x: Image.fromarray(255 * x)))
        self.update_geometry(self.pixmap.width(), self.pixmap.height(), x=self.PADDING, y=self.label.pos().y())

        self.extra_action_button = self.add_button("Median filter",
                                                   lambda x: QTimer.singleShot(100, lambda: self.update_median()),
                                                   setEnabled=False)
        self.update_geometry(self.pixmap.width(), 30, x=self.PADDING, y=self.action_button.pos().y())

        # need to set a mask first
        self.action_button.setEnabled(False)

    def pixmap_handler(self, data) -> Array:
        """
        Makes sure the pixel format is correct

        Parameters
        ----------
        data : ndarray
            The data to convert to correct format

        Returns
        -------
        ndarray
            The converted image to a format QImage likes
        """
        return ((lambda x: self.pixmap_converter(x))) if not self.pixmap_converter is None else (
            lambda x: Image.fromarray((255 * x).astype(np.uint8)))(data)

    def update_median(self):
        """
        Update the median image
        """
        self.setWindowTitle("Calculating...")
        QApplication.processEvents()
        self.extra_label.setPixmap(pil2pixmap(self.pixmap_handler(median_filter(self.input_image, self.method.mask))))
        self.setWindowTitle(self.title)

    @pyqtSlot()
    def reset_image(self):
        """
        Resets the image
        """
        self.epoch_label.setText("Epochs")
        self.total_epochs = 0
        self.method.reset()
        self.update_image_label()
        self.extra_action_button.setEnabled(False)
        self.action_button.setEnabled(False)
        self.noise_button.setEnabled(True)
        self.reset_button.setEnabled(False)

    def update_image_noise(self):
        """
        Update the image after noise was added
        """
        self.method.destroy_information(self.noise_slider.value())
        self.extra_label.setPixmap(pil2pixmap(self.pixmap_handler(self.method.data)))
        self.label.setPixmap(pil2pixmap(self.pixmap_handler(self.method.data)))

        self.extra_action_button.setEnabled(True)
        self.action_button.setEnabled(True)
        self.noise_button.setEnabled(False)
        self.reset_button.setEnabled(True)
