from PyQt5.QtCore import pyqtSlot

from backend import demosaicing
from gui.general_window import *
from gui.general import *

import numpy as np

class demonsaic_window(general_window):
    """
    This class describes a demonsaic window.
    """

    def __init__(self, parent=None):
        general_window.__init__(self, (lambda x: Image.fromarray((x * 255).astype(np.uint8))),
                                load_extra=lambda: self.load_extra_now())
        self.method = demosaicing.Demosaic(self.image, color=True)
        self.input_image = self.method.get_data().copy()

    def load_extra_now(self):
        """
        add the mosaic button
        """
        self.mosaic_button = self.add_button('Mosaic', lambda x: QTimer.singleShot(100, lambda: self.update_simulate()))
        self.update_geometry(self.pixmap.width(), 30)
        self.action_button.setEnabled(False)

    @pyqtSlot()
    def reset_image(self):
        """
        Resets the image
        """
        self.epoch_label.setText("Epochs")
        self.total_epochs = 0
        self.method.reset()
        self.action_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))

    def update_simulate(self):
        """
        Update the simulation
        """
        self.label.setPixmap(pil2pixmap(Image.fromarray((self.method.simulate() * 255).astype(np.uint8))))
        self.action_button.setEnabled(True)
