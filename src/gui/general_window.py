from gui.app_data import App, pil2pixmap
from gui.interface import interface_class
from PIL import Image
import numpy as np
from PyQt5.QtCore import QTimer

class general_window(interface_class):
	"""
	Convers the input into a format QT liks

	Parameters
	----------
	pixmap_converter : lambda
		a lambda function used to parse a image into QT
	load_extra : lambda
		a lambda function used to parse a load extra content
	"""
	def __init__(self, pixmap_converter=None, load_extra=None, load_before=None):
		interface_class.__init__(self)
		self.pixmap_converter = pixmap_converter
		self.load_extra = load_extra
		self.load_before = load_before

	def init_UI(self):
		"""
		initialize the UI
		"""
		self.setWindowTitle(self.title)
		"""
		Showing the possible modes
		"""
		self.mode = self.add_mode_switch(action=self.mode_change, element_id="mode")

		"""
		Showing the image
		"""
		self.label, self.pixmap = self.add_image(self.method.data, (
			lambda x: self.pixmap_converter(x)) if not self.pixmap_converter is None else (
			lambda x: Image.fromarray(255 * x)))
		self.update_geometry(self.pixmap.width(), self.pixmap.height(), y=30)
		self.update_geometry(self.pixmap.width(), 20, element_id="mode", y=5)

		"""
		Make sure elements that should be loaded before is laoded
		"""
		if not self.load_before is None:
			self.load_before(None)

		"""
		Showing the boundary box options
		"""
		self.boundary_group = None
		self.method_group = None
		
		self.boundary_box, self.boundary_group = self.add_radio_buttons("Boundary", [
				"Neumann", "Dirichlet"
			], self.boundary_change, 0)
		print(self.boundary_box)
		self.update_geometry(self.boundary_box.width(), 90, x=10)

		"""
		Showing the method box options
		"""
		self.boundary_box, self.method_group = self.add_radio_buttons("Method", [
				"Explicit", "Implicit"
			], self.method_change, 0)
		self.update_geometry(self.boundary_box.width(), 90, x=10)

		"""
		Showing the Alpha label
		"""
		self.alpha_label = self.add_label("Alpha")
		self.update_geometry(self.pixmap.width(), 30, x=10)

		"""
		Showing the epoch slider
		"""
		self.alpha_slider = self.add_slider('Alpha', action=self.alpha_chnage)
		self.update_geometry(self.pixmap.width(), 30)

		"""
		Showing the epoch count label
		"""
		self.epoch_label = self.add_label("epochs")
		self.update_geometry(self.pixmap.width(), 30, x=10)

		"""
		Showing the epoch slider
		"""
		self.epoch_slider = self.add_slider('How many epochs to run for?', action=self.epochs_change)
		self.update_geometry(self.pixmap.width(), 30)


		"""
		Showing the run button
		"""
		self.action_button = self.add_button("Run", self.run_method)
		self.update_geometry(self.pixmap.width(), 30)
		"""
		Showing the reset button
		"""
		self.reset_button = self.add_button("Reset", lambda x: QTimer.singleShot(100, lambda: self.reset_image()),
											setEnabled=False)
		self.update_geometry(self.pixmap.width(), 30)

		"""
		Showing the custom file button
		"""
		self.open_button = self.add_button("Open", lambda x: QTimer.singleShot(100, lambda: self.show_file_dialog()),
											setEnabled=True)
		self.update_geometry(self.pixmap.width(), 30)

		"""
		Position all the elements
		"""
		if not self.load_extra is None:
			self.load_extra(None)

		width, height = self.position()
		self.setGeometry(0, 0, width, height)
		self.center()
#	self.setFixedSize(self.size())
