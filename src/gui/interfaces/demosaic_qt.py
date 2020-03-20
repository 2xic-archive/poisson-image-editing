from backend import demosaicing
from gui.general_window import *


class demonsaic_window(general_window):
    def __init__(self, parent=None):
        general_window.__init__(self, (lambda x: Image.fromarray((x * 255).astype(np.uint8))),
                                load_extra=lambda x: self.load_extra_now())
        self.method = demosaicing.demosaic(self.image, color=True)
        self.input_image = self.method.get_data().copy()

    def load_extra_now(self):
        self.mosaic_button = self.add_button('Mosaic', lambda x: QTimer.singleShot(100, lambda: self.update_simulate()))
        self.update_geometry(self.pixmap.width(), 30)

    def update_simulate(self):
        self.label.setPixmap(pil2pixmap(Image.fromarray((self.method.simulate() * 255).astype(np.uint8))))
