from backend import contrasting
from gui.general_window import *
from extra.local_adaptive_histogram import *


class contrast_window(general_window):
	"""
	This class describes a contrast window.
	"""
	def __init__(self, parent=None):
		general_window.__init__(self, load_extra=lambda x: self.load_extra_now())
		self.image = './files/test_images/contrast.jpg'
		self.method = contrasting.Contrast(self.image)
		self.input_image = self.method.get_data().copy()
		self.height = 0

	def load_extra_now(self):
		"""
		Load the extra
		"""
		_, self.heigth = self.position()
		self.extra_button = self.add_button("Extra", lambda x: QTimer.singleShot(100, lambda: self.show_extra_la()))
		self.update_geometry(self.pixmap.width(), 30)

		self.PADDING = self.pixmap.width() + 30

		self.extra_label, self.extra_pixmap = self.add_image(self.method.data, (
			lambda x: self.pixmap_converter(x)) if not self.pixmap_converter is None else (
			lambda x: Image.fromarray(255 * x)))
		self.update_geometry(self.pixmap.width(), self.pixmap.height(), x=self.PADDING, y=self.label.pos().y())

		self.extra_action_button = self.add_button("Local adaptive histogram", lambda x: QTimer.singleShot(100, lambda: self.update_image_histogram()))
		self.update_geometry(self.pixmap.width(), 30, x=self.PADDING, y=self.action_button.pos().y())

	def update_image_histogram(self):
		"""
		Update the histogram label
		"""
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * contrast_enhancement(self.input_image))))

	def show_extra_la(self):
		"""
		Resize the window
		"""
		self.setGeometry(0, 0, self.pixmap.width() + self.PADDING, self.heigth)
		self.center()
