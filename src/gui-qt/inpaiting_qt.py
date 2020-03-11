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
from extra.median_filter import median_filter

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
		self.pixmap = pil2pixmap(Image.fromarray(255 * self.inpait.data))
		self.label.setPixmap(self.pixmap)
		#self.resize(self.pixmap.width(), self.pixmap.height() + 100)
		#self.move(0, 30)
		self.label.setGeometry(0, 30, self.pixmap.width(), self.pixmap.height());

		self.noise_label = QLabel(self)
		self.noise_label.setText("Remove information")
		self.noise_label.setGeometry(0, self.pixmap.height() + 30, self.pixmap.width(), 30)

		self.noiseSlider = QSlider(Qt.Horizontal, self)
		self.noiseSlider.setMinimum(1)
		self.noiseSlider.setMaximum(10)
		self.noiseSlider.setSingleStep(1)
		self.noiseSlider.setGeometry(0, self.pixmap.height() + 60, self.pixmap.width(), 30)
		self.noiseSlider.setToolTip('How much information to remove?')
		#self.noiseSlider.valueChanged.connect(self.epochsChange)

		self.noise_button = QPushButton('Remove', self)
		self.noise_button.move(0, self.pixmap.height() + 85)
		self.noise_button.clicked.connect(self.action_add_noise)

		self.epoch_label = QLabel(self)
		self.epoch_label.setText("Epochs")
		self.epoch_label.setGeometry(0, self.pixmap.height() + 110, self.pixmap.width(), 30)

		self.epochSlider = QSlider(Qt.Horizontal, self)
		self.epochSlider.setMinimum(1)
		self.epochSlider.setMaximum(10)
		self.epochSlider.setSingleStep(1)		
		self.epochSlider.setGeometry(0, self.pixmap.height() + 140, self.pixmap.width(), 30)
		self.epochSlider.setToolTip('How many epochs to run for?')
		self.epochSlider.valueChanged.connect(self.epochsChange)

		self.action_button = QPushButton('Run', self)
		self.action_button.move(self.action_button.frameGeometry().width() // 2, self.pixmap.height() + 160)
		self.action_button.clicked.connect(self.on_click)
		self.action_button.setEnabled(False)

		self.mode = QComboBox(self)
#		self.mode.addItem("inpaitring")
#		self.mode.addItem("inpait")
		self.mode.setGeometry(0, 0, self.pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.modeChange)

		self.timer = QTimer(self)
		self.i =0
		

		"""
			TODO : Chck if you can add this element later in the launch
		"""
		self.extra_button = QPushButton('Extra', self)
		self.extra_button.move(self.extra_button.frameGeometry().width(), self.pixmap.height() + 85)
		self.extra_button.clicked.connect(self.showExtra)

		PADDING = self.pixmap.width()
		self.extra_label = QLabel(self)
		self.extra_pixmap = pil2pixmap(Image.fromarray(255 * self.inpait.data))
		self.extra_label.setPixmap(self.pixmap)
		self.extra_label.setGeometry(PADDING, 30, self.extra_pixmap.width(), self.extra_pixmap.height());

		self.extra_action_button = QPushButton('Median filter', self)
		self.extra_action_button.move(PADDING + self.extra_action_button.frameGeometry().width() // 2, self.pixmap.height() + 160)
		self.extra_action_button.clicked.connect(self.median)

	#	QTimer.singleShot(100, lambda: self.action_button.setEnabled(False) or print("happy"))


		self.run = False
		self.setGeometry(0, 0 , self.pixmap.width(), self.pixmap.height() + 200)
		self.center()

	def update_median(self):
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * median_filter(self.inpait.data.copy()))))
		self.timer.stop()

	@pyqtSlot()
	def median(self):
#		self.i = 0
		self.timer.timeout.connect(self.update_median)
		self.timer.start(100)
		
	def epochsChange(self):
		size = self.epochSlider.value()
		self.epoch_label.setText("Epochs ({})".format(size))

	@pyqtSlot()
	def action_add_noise(self):
		self.run = False
		self.inpait.destroy_information(self.noiseSlider.value())		
		QTimer.singleShot(100, lambda: self.update_image_noise())

	def update_image_noise(self):
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * self.inpait.data)))
		self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.inpait.data)))
		self.action_button.setEnabled(True)
		self.noise_button.setEnabled(False)
			
	def update_image(self):
		if(self.i < self.epochSlider.value()):
			self.inpait.fit(1)
			self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.inpait.data)))
			self.i += 1
		else:	
			self.run = True
			self.timer.stop()			

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

