from gui.general_window import *
from backend import blurring
from PyQt5 import QtCore

class blur_window(general_window):
	"""
	This class describes a blur window.
	"""
	def __init__(self, parent=None):
		general_window.__init__(self, load_before=lambda x: self.load_extra_now())
		self.method = blurring.blur(self.image)

	def load_extra_now(self):
		"""
		Adds the option for data attacment
		"""
		self.data_attachment_label = self.add_label("Data attachment")
		self.update_geometry(self.pixmap.height(), 30, x=10)

		self.lambda_size = self.add_slider("How strong should the blur be?", self.epochs_change)
		self.update_geometry(self.pixmap.height(), 30)

		self.data_attachemnt = self.add_button("Data attachment", lambda x: QTimer.singleShot(100, lambda: self.update_image_noise()))
		self.update_geometry(self.pixmap.height(), 30)	

		"""
		Turn off or on the colors
		"""
		self.color_checkbox = self.add_checkbox('Use color?', action=self.update_image_color) 
		self.update_geometry(self.pixmap.width(), 30)

	def update_image_color(self, state):
		#if state == QtCore.Qt.Checked:
		#	print("uf")
#			print(self.method.data)
		self.method.change_color_state()
		self.update_image_label()
#			print(self.method.data)
	#		self.update_image_noise()
#		else:
#			print("ye")	

	def update_image_noise(self):
		self.method.set_lambda_size(self.lambda_size.value()/10 )
		self.run_method()