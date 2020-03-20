import blurring
#from main import *
from general_window import *

class blur_window(general_window):
	def __init__(self, parent=None):	
		general_window.__init__(self)
		self.method = blurring.blur(self.image)
	'''
	self.blur = blurring.blur(self.image)
	def initUI(self):
		self.setWindowTitle(self.title)
		"""
		Showing the possible modes
		"""
		self.mode = self.add_mode_switch(action=self.mode_change, element_id="mode")

		"""
		Showing the image
		"""
		self.label, self.pixmap = self.add_image(self.blur.data)
		self.update_geometry(self.pixmap.width(), self.pixmap.height())
		self.update_geometry(self.pixmap.width(), 20, element_id="mode", y=30)

		"""
		Showing the epoch count label
		"""
		self.epoch_label = self.add_label("epochs")
		self.update_geometry(self.pixmap.width(), 30, x=10)

		"""
		Showing the epoch slider
		"""		
		self.epochSlider = self.add_slider(action=self.epochs_change)
		self.update_geometry(self.pixmap.width(), 30)

		"""
		Showing the run button
		"""
		self.action_button = self.add_button("Run", self.run_method)
		self.update_geometry(self.pixmap.width(), 30)
		"""
		Showing the run reset
		"""
		self.reset_button = self.add_button("Reset", lambda x: QTimer.singleShot(100, lambda: self.reset_image()), setEnabled=False)
		self.update_geometry(self.pixmap.width(), 30)			

		"""
		Position all the elements
		"""
		width, height = self.position()
		self.setGeometry(0, 0 , width, height)
		self.center()
		self.setFixedSize(self.size())
	'''


