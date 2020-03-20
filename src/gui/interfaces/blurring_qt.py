#import .blurring
from gui.general_window import *
from backend import blurring

class blur_window(general_window):
    def __init__(self, parent=None):
        general_window.__init__(self)
        self.method = blurring.blur(self.image)
