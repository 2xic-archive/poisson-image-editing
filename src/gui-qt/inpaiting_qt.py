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
from PIL import Image
from main import App
import inpaiting
from general import pil2pixmap

class inpait_window(App):
	def __init__(self, parent=None):	
		super(App, self).__init__(parent)

		self.image = '../test_images/lena.png'
		self.title = self.image

		self.inpait = inpaiting.inpait(self.image)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)

		self.label = QLabel(self)
		pixmap = pil2pixmap(Image.fromarray(255 * self.inpait.data))
		self.label.setPixmap(pixmap)
		#self.resize(pixmap.width(), pixmap.height() + 100)
		#self.move(0, 30)
		self.label.setGeometry(0, 30, pixmap.width(), pixmap.height());

		self.noise_label = QLabel(self)
		self.noise_label.setText("Remove information")
		self.noise_label.setGeometry(0, pixmap.height() + 30, pixmap.width(), 30)

		self.noiseSlider = QSlider(Qt.Horizontal, self)
		self.noiseSlider.setMinimum(1)
		self.noiseSlider.setMaximum(10)
		self.noiseSlider.setSingleStep(1)
		self.noiseSlider.setGeometry(0, pixmap.height() + 60, pixmap.width(), 30)
		self.noiseSlider.setToolTip('How much information to remove?')
		#self.noiseSlider.valueChanged.connect(self.epochsChange)

		self.noise_button = QPushButton('Remove', self)
		self.noise_button.move(self.noise_button.frameGeometry().width() // 2, pixmap.height() + 85)
		self.noise_button.clicked.connect(self.action_add_noise)

		self.epoch_label = QLabel(self)
		self.epoch_label.setText("Epochs")
		self.epoch_label.setGeometry(0, pixmap.height() + 110, pixmap.width(), 30)

		self.epochSlider = QSlider(Qt.Horizontal, self)
		self.epochSlider.setMinimum(1)
		self.epochSlider.setMaximum(10)
		self.epochSlider.setSingleStep(1)		
		self.epochSlider.setGeometry(0, pixmap.height() + 140, pixmap.width(), 30)
		self.epochSlider.setToolTip('How many epochs to run for?')
		self.epochSlider.valueChanged.connect(self.epochsChange)

		self.action_button = QPushButton('Run', self)
		self.action_button.move(self.action_button.frameGeometry().width() // 2, pixmap.height() + 160)
		self.action_button.clicked.connect(self.on_click)

		self.mode = QComboBox(self)
#		self.mode.addItem("inpaitring")
#		self.mode.addItem("inpait")
		self.mode.setGeometry(0, 0, pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.modeChange)

		self.timer = QTimer(self)
		self.i =0
		
		self.action_button.setEnabled(False)

		self.run = False
		self.setGeometry(0, 0 , pixmap.width(), pixmap.height() + 200)
		self.center()

	@pyqtSlot()
	def action_add_noise(self):
		print("hou")
		self.noise_button.setEnabled(False)
		self.inpait.destroy_information(self.noiseSlider.value())
		self.run = False

		self.timer.timeout.connect(self.update_image)
		self.timer.start(100)
		self.action_button.setEnabled(True)

	def update_image(self):
		if(self.i < self.epochSlider.value()):
			if(self.run):
				self.action_button.setEnabled(False)
				self.inpait.fit(1)
			self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.inpait.data)))
			self.i += 1
		else:	
			self.timer.stop()
			self.action_button.setEnabled(True)
			self.run = True


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

