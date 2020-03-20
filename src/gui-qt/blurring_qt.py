import blurring
from general_window import *

class blur_window(general_window):
	def __init__(self, parent=None):	
		general_window.__init__(self,l)
		self.method = blurring.blur(self.image)