from backend import inpaiting
from gui.general_window import *
from extra.median_filter import median_filter

from PyQt5.QtCore import pyqtSlot

class inpait_window(general_window):
	"""
	This class describes an inpait window.
	"""
	def __init__(self, parent=None):	
		general_window.__init__(self, load_extra=lambda x: self.load_extra_now(), load_before=lambda x: self.load_before_now())
		self.method = inpaiting.inpaint(self.image)
		self.input_image = self.method.get_data().copy()

	def load_before_now(self):
		"""
		Adds the option to remove information
		"""
		self.noise_label = self.add_label("Remove information")
		self.update_geometry(self.pixmap.height(), 30)

		self.noise_slider = self.add_slider("How much information to remove?", self.epochs_change)
		self.update_geometry(self.pixmap.height(), 30)

		self.noise_button = self.add_button("Remove", lambda x: QTimer.singleShot(100, lambda: self.update_image_noise()))
		self.update_geometry(self.pixmap.height(), 30)		

	def load_extra_now(self):
		"""
		Generate the extra row
		"""
		_, self.height = self.position()
		self.PADDING = self.pixmap.width() + 30

		self.extra_button = self.add_button("Extra", lambda x: QTimer.singleShot(100, lambda: self.show_extra()))
		self.update_geometry(self.pixmap.width(), 30)			

		self.extra_label, self.extra_pixmap = self.add_image(self.method.data, (lambda x : self.pixmap_converter(x)) if not self.pixmap_converter is None else (lambda x: Image.fromarray(255 * x)))
		self.update_geometry(self.pixmap.width(), self.pixmap.height(), x=self.PADDING, y=self.label.pos().y())

		self.extra_action_button = self.add_button("Median filter", lambda x: QTimer.singleShot(100, lambda: self.update_median()))
		self.update_geometry(self.pixmap.width(), 30, x=self.PADDING, y=self.action_button.pos().y())			

	def pixmap_handler(self, data):
		return  (self.pixmap_converter(x)) if not self.pixmap_converter is None else (lambda x: Image.fromarray(255 * x))(data)

	def update_median(self):
		"""
		Update the median image
		"""
		print(pil2pixmap, self.pixmap_converter, median_filter, self.input_image)
		self.extra_label.setPixmap(pil2pixmap(self.pixmap_handler(median_filter(self.input_image))))
		
	@pyqtSlot()
	def reset_image(self):
		"""
		Resets the image
		"""
		self.epoch_label.setText("Epochs")
		self.total_epochs = 0
		self.method.reset()
		self.action_button.setEnabled(False)
		self.noise_button.setEnabled(True)

	def update_image_noise(self):
		"""
		Update the image after noise was added
		"""
		self.method.destroy_information(self.noise_slider.value())		
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * self.method.data)))
		self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.method.data)))

		self.extra_action_button.setEnabled(True)
		self.action_button.setEnabled(True)
		self.noise_button.setEnabled(False)
		self.reset_button.setEnabled(True)
