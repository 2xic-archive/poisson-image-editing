import anonymizing
from general_window import *

class anonymizing_window(general_window):
	def __init__(self, parent=None):	
		general_window.__init__(self)
		self.method = anonymizing.anonymous(self.image)
