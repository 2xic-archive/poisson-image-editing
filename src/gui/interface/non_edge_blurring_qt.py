import non_edge_blurring
from general_window import *


class non_edge_blurring_window(general_window):
    def __init__(self, parent=None):
        general_window.__init__(self)
        self.method = non_edge_blurring.non_edge_blurr(self.image)