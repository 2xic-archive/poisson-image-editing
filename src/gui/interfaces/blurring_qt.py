#import .blurring
from gui.general_window import *
from backend import blurring

class blur_window(general_window):
	"""
	This class describes a blur window.
	"""
	def __init__(self, parent=None):
		general_window.__init__(self, load_extra=lambda x: self.load_extra_now())
		self.method = blurring.blur(self.image)

	def load_extra_now(self):
		"""
		Adds the option for data attacment
		"""
		self.data_attachment_label = self.add_label("Data attachment")
		self.update_geometry(self.pixmap.height(), 30)

		self.lambda_size = self.add_slider("How strong should the blur be?", self.epochs_change)
		self.update_geometry(self.pixmap.height(), 30)

		self.data_attachemnt = self.add_button("Data attachment", lambda x: QTimer.singleShot(100, lambda: self.update_image_noise()))
		self.update_geometry(self.pixmap.height(), 30)	

	def update_image_noise(self):
		self.method.set_lambda_size(self.lambda_size.value()/10 )
		self.run_method()