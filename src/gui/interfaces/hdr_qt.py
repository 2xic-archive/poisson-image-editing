from backend import hdr_reconstruction
#from engine import hdr_image_handler
from gui.general_window import *

class hdr_window(general_window):
	"""
	This class describes a header window.
	"""
	def __init__(self, parent=None):
		general_window.__init__(self,  (lambda x: Image.fromarray((x * 255).astype(np.uint8))))

		self.method = hdr_reconstruction.hdr_reconstruction()#'../hdr-bilder/Adjuster/Adjuster_00064.png')