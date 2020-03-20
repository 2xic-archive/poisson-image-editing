from backend import hdr_reconstruction
from gui.general_window import *

class hdr_window(general_window):
    def __init__(self, parent=None):
        general_window.__init__(self)
        self.method = hdr_reconstruction.hdr_reconstruction(self.image)