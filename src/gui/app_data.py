import time
import numpy as np
from PIL import Image
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtWidgets import QMainWindow
from gui.general import *


class App(QMainWindow):
	"""
	Standard application interface

	Parameters
	----------
	image : ndarray
		The image to open
	"""
	image: str
	title: str
	total_epochs: int
	epoch: int

	def __init__(self, image='./files/test_images/lena.png'):
		super().__init__()
		self.image = image
		self.title = os.path.basename(self.image)


		self.epoch = 0
		self.total_epochs = 0
		self.timer = QTimer(self)


	def get_available_windows(self, INFILE):
		"""
		Get all the windows

		Parameters
		----------
		INFILE : str
			Makes sure we don't reload the file recursively
		"""
		global WINDOW_MANAGER
		return WINDOW_MANAGER.filter(INFILE)

	#   https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
	def center(self):
		"""
		Center the window

		"""
		frame_geometry = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		center = QApplication.desktop().screenGeometry(screen).center()
		frame_geometry.moveCenter(center)
		self.move(frame_geometry.topLeft())

	def epochs_change(self):
		"""
		Updates the epoch label
		"""
		epochs: int = self.epochSlider.value()
		self.epoch_label.setText("Epochs ({}) (Total {})".format(epochs, self.total_epochs))

	def mode_change(self, _):
		"""
		Changes the view from the combobox
		"""
		view = self.WINDOWS[self.mode.currentText()]
		view.init_UI()
		view.show()
		self.hide()

	@pyqtSlot()
	def update_image_label(self):
		 self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))   

	def update_image(self):
		"""
		Wrapper to nicely update the image when preform a iteration from the backend
		"""
		if self.epoch < self.epochSlider.value():
			self.method.fit(epochs=1)
			self.update_image_label()
			self.epoch += 1
			self.total_epochs += 1
			self.epochs_change()
			self.reset_button.setEnabled(True)
		else:
			self.reset_button.setEnabled(True)
			self.timer.stop()

	def show_file_dialog(self):
		"""
		Shows a file dialog
		"""
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
												  "All Files (*);;JPEG (*.jpeg);;jpg (*.jpg);;png (*.png)",
												  options=options)
		if file_name:
			"""
			TODO : Add custom files
			Should not be 2 hard, however we have to figure how the image should be displayed as QT else will crash
			"""
			# self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))
			raise Exception("Feature is not fully implemented (yet)")

	def show_extra(self):
		"""
		Shows the extra features
		"""
		self.setGeometry(0, 0, self.pixmap.width() + self.PADDING, self.height)
		self.center()

	def screenshot(self):
		"""
		Takes a screenshot of the current QWindow
		"""
		screen = self.grab()
		screen.save("{}.png".format(time.time()), 'png')

	@pyqtSlot()
	def reset_image_extra(self):
		"""
		Resets the image
		"""
		self.total_epochs = 0
		self.epoch_label.setText("Epochs")

		self.reset_button.setEnabled(False)
		self.method.reset()
		self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))

	@pyqtSlot()
	def run_method(self):
		"""
		Runs one of the backends methods
		"""
		self.epoch = 0
		self.timer.timeout.connect(self.update_image)
		self.timer.start(100)

	def reset_image(self):
		"""
		Resets the image
		"""
		self.epoch_label.setText("Epochs")
		self.total_epochs = 0
		self.reset_button.setEnabled(False)
		self.method.reset()
		self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))





