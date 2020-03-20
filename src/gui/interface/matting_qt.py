import matting
from general_window import *


class matting_window(general_window):
    def __init__(self, parent=None):
        general_window.__init__(self, lambda x: Image.fromarray((x * 255).astype(np.uint8), mode='RGBA'))
        self.method = matting.matting(self.image)
