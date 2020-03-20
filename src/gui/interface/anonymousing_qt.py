import anonymousing
from general_window import *

class anonymous_window(general_window):
	def __init__(self, parent=None):	
		general_window.__init__(self)
		self.method = anonymousing.anonymous(self.image)
