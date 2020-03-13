import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QTimer
from PIL.ImageQt import ImageQt
from PIL import Image
import numpy as np

import os
import sys
sys.path.append("../")

import blurring
from PIL import Image
from general import *

class App(QMainWindow):

	def __init__(self, parrent=None):
		super().__init__()
		self.image = '../test_images/lena.png'
		self.title = self.image
		self.left = 0
		self.top = 0
		self.width = 640
		self.height = 480

		self.epoch = 0
		self.timer = QTimer(self)

	def get_avaible_windows(self, INFILE):
		self.WINDOWS = {
		}
		import blurring_qt as blur_window
		import inpaiting_qt as inpait_window
		import contrast_qt as contrast_window
		import demonsaic_qt as demonsaic_window
		if (blur_window.__file__ not in INFILE):
			self.WINDOWS["Blurring"] = blur_window.blur_window()
		if (inpait_window.__file__ not in INFILE):
			self.WINDOWS["Inpaiting"] = inpait_window.inpait_window()
		if (contrast_window.__file__ not in INFILE):
			self.WINDOWS["Contrasting"] = contrast_window.contrast_window()
		if (demonsaic_window.__file__ not in INFILE):
			self.WINDOWS["Demonsaicing"] = demonsaic_window.demonsaic_window()
		return self.WINDOWS

	#	https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def epochs_change(self):
		size = self.epochSlider.value()
		self.epoch_label.setText("Epochs ({})".format(size))

	def mode_change(self, _):
		NEW_VIEW = (self.mode.currentText())
		VIEW = self.WINDOWS.get(NEW_VIEW, None)
		if(VIEW == None):
			print("not ready")
		else:
			VIEW.initUI()
			VIEW.show()
			self.hide()

	def update_image(self):
		if(self.epoch < self.epochSlider.value()):
			self.method.fit(1)
			self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.method.data)))
			self.epoch += 1
		else:	
			self.reset_button.setEnabled(True)
			self.timer.stop()

	@pyqtSlot()
	def reset_image(self):
		self.reset_button.setEnabled(False)
		self.method.reset()
		self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.method.data)))

	@pyqtSlot()
	def run_method(self):
		self.epoch = 0
		self.timer.timeout.connect(self.update_image)
		self.timer.start(100)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	from blurring_qt import blur_window
	ex = blur_window()
	ex.initUI()
	ex.show()
	sys.exit(app.exec_())

