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

		import blurring_qt as blur_window
		import inpaiting_qt as inpait_window

		self.blak = blurring.blur(self.image)
		self.WINDOWS = {
			"Blurring":blur_window.blur_window(),
			"Inpaiting": inpait_window.inpait_window()
		}


		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)

		self.label = QLabel(self)
		pixmap = pil2pixmap(Image.fromarray(255 * self.blak.data))
		self.label.setPixmap(pixmap)
		self.label.setGeometry(0, 30, pixmap.width(), pixmap.height());

		self.mode = QComboBox(self)
		for keys in self.WINDOWS.keys():
			self.mode.addItem(keys)

		self.mode.setGeometry(0, 0, pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.modeChange)

		self.setGeometry(self.left, self.top, pixmap.width(), pixmap.height() + 150)
		self.center()

	#	https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

#	informing the user
	def epochsChange(self):
		size = self.epochSlider.value()
		self.epoch_label.setText("Epochs ({})".format(size))

	def modeChange(self, i):
		NEW_VIEW = (self.mode.currentText())
		VIEW = self.WINDOWS.get(NEW_VIEW, None)
		if(VIEW == None):
			print("not ready")
		else:
			VIEW.show()
			self.hide()

	@pyqtSlot()
	def on_click(self):
		self.i = 0
		self.timer.timeout.connect(self.update_image)
		self.timer.start(100)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	sys.exit(app.exec_())

