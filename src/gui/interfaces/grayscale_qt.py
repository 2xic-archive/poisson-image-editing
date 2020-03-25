import backend
from gui.general_window import *


class grayscale_window(general_window):
	"""
	This class describes a grayscale window.
	"""
	def __init__(self, parent=None):
		general_window.__init__(self, (lambda x: Image.fromarray((x * 255).astype(np.uint8))))
		self.method = backend.grayscale.grayscale(self.image)
