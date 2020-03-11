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
from main import App
from general import pil2pixmap

class blur_window(App):
	def __init__(self, parent=None):	
		super(App, self).__init__(parent)

		self.image = '../test_images/lena.png'
		self.title = self.image

		self.blur = blurring.blur(self.image)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)

		self.label = QLabel(self)
		pixmap = pil2pixmap(Image.fromarray(255 * self.blur.data))
		self.label.setPixmap(pixmap)
		#self.resize(pixmap.width(), pixmap.height() + 100)
		#self.move(0, 30)
		self.label.setGeometry(0, 30, pixmap.width(), pixmap.height());

		self.epoch_label = QLabel(self)
		self.epoch_label.setText("Epochs")
		self.epoch_label.setGeometry(0, pixmap.height() + 35, pixmap.width(), 30)

		self.epochSlider = QSlider(Qt.Horizontal, self)
		self.epochSlider.setMinimum(1)
		self.epochSlider.setMaximum(10)
		self.epochSlider.setSingleStep(1)
		
		self.epochSlider.setGeometry(0, pixmap.height() + 65, pixmap.width(), 30)
		self.epochSlider.setToolTip('How many epochs to run for?')
		self.epochSlider.valueChanged.connect(self.epochsChange)

		self.action_button = QPushButton('Run', self)
		self.action_button.move(self.action_button.frameGeometry().width() // 2, pixmap.height() + 100)
		self.action_button.clicked.connect(self.on_click)


		self.mode = QComboBox(self)
		self.mode.addItem("blurring")
		self.mode.addItem("inpait")
		self.mode.setGeometry(0, 0, pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.modeChange)

		self.timer = QTimer(self)
		self.i = 0

		self.setGeometry(0, 0 , pixmap.width(), pixmap.height() + 150)
		self.center()

	def update_image(self):
		if(self.i < self.epochSlider.value()):
			self.action_button.setEnabled(False)
			self.blur.fit(1)
			self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.blur.data)))
			self.i += 1
		else:	
			self.timer.stop()
			self.action_button.setEnabled(True)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

