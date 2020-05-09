from backend import hdr_reconstruction
from gui.general_window import *
from gui.interface import interface_class

class hdr_window(interface_class):
	"""
	This class describes a header window.
	"""
	def __init__(self, parent=None):
		interface_class.__init__(self)
		self.method = hdr_reconstruction.hdr_reconstruction()
		self.pixmap_converter = (lambda x: Image.fromarray((x * 255).astype(np.uint8)))
		
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
		Showing the run button
		"""
		self.action_button = self.add_button("Run", lambda x: self.run_method(True))
		self.update_geometry(self.pixmap.width(), 30)

		"""
		Showing the custom file button
		"""
		self.open_button = self.add_button("Open", lambda x: QTimer.singleShot(100, lambda: self.show_file_dialog_hdr()),
											setEnabled=True)
		self.update_geometry(self.pixmap.width(), 30)

		"""
		Showing the reset button
		"""
		self.reset_button = self.add_button("Reset", lambda x: QTimer.singleShot(100, lambda: self.reset_image()),
											setEnabled=False)
		self.update_geometry(self.pixmap.width(), 30)

		width, height = self.position()
		self.setGeometry(0, 0, width, height)
		self.center()