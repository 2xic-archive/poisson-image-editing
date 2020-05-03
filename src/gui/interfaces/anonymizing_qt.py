from backend import anonymizing
from gui.general_window import *


class anonymizing_window(general_window):
	"""
	This class describes an anonymizing window.
	"""
	def __init__(self, parent=None):
		general_window.__init__(self,  lambda x: Image.fromarray((x * 255).astype(np.uint8)))
		self.method = anonymizing.anonymous(self.image)
