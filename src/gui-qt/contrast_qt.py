import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox#, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QMainWindow, QCheckBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QTimer
from PIL.ImageQt import ImageQt
from PIL import Image
import numpy as np

import os
import sys
sys.path.append("../")
from extra.local_adaptive_histogram import *

from PyQt5.QtWidgets import QFrame
import blurring
from PIL import Image
from PIL import Image
from main import App
import contrasting
from general import pil2pixmap

class contrast_window(App):
	def __init__(self, parent=None):	
		super(App, self).__init__(parent)

		self.image = '../test_images/contrast.jpg'
		self.title = self.image

		self.contrast = contrasting.contrast(self.image)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)

		self.label = QLabel(self)
		self.pixmap = pil2pixmap(Image.fromarray(255 * self.contrast.data))
		self.label.setPixmap(self.pixmap)
		#self.resize(self.pixmap.width(), self.pixmap.height() + 100)
		#self.move(0, 30)
		self.label.setGeometry(0, 30, self.pixmap.width(), self.pixmap.height());
		'''
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
		'''
		
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


		self.mode = QComboBox(self)
		self.mode.setGeometry(0, 0, self.pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.modeChange)

		self.timer = QTimer(self)
		self.i = 0

		"""
			TODO : Chck if you can add this element later in the launch
		"""
		self.extra_button = QPushButton('Extra', self)
		self.extra_button.move(self.extra_button.frameGeometry().width() // 2, self.pixmap.height() + 85)
		self.extra_button.clicked.connect(self.showExtra)

		PADDING = self.pixmap.width()
		self.extra_label = QLabel(self)
		self.extra_pixmap = pil2pixmap(Image.fromarray(255 * self.contrast.data))
		self.extra_label.setPixmap(self.pixmap)
		self.extra_label.setGeometry(PADDING, 30, self.extra_pixmap.width(), self.extra_pixmap.height());

		self.action_button = QPushButton('Local adaptive histogram', self)
		self.action_button.move(PADDING + self.action_button.frameGeometry().width() // 2, self.pixmap.height() + 160)
		self.action_button.clicked.connect(self.histogram)
		
		self.setGeometry(0, 0 , self.pixmap.width(), self.pixmap.height() + 200)
		self.center()

#	@pyqtSlot()
#	def updateExtra(self):
#		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * contrast_enhancment(self.contrast.data))))
#		self.timer.stop()
#		print("ye")


	def update_image_histogram(self):
		#	contrast_enhancment
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * contrast_enhancment(self.contrast.data))))
		self.timer.stop()

	@pyqtSlot()
	def histogram(self):
		self.i = 0
		self.timer.timeout.connect(self.update_image_histogram)
		self.timer.start(100)

	def showExtra(self):
		self.setGeometry(0, 0 , self.pixmap.width() + 200, self.pixmap.height() + 200)
		self.center()

#		self.timer.timeout.connect(self.updateExtra)
#		self.timer.start(100)


		# from https://stackoverflow.com/questions/50825126/how-to-increase-qframe-hline-line-separator-width-and-distance-with-the-other-bu
#		self.separatorLine = QFrame()
#		self.separatorLine.setFrameShape( QFrame.HLine )
#		self.separatorLine.setFrameShadow( QFrame.Raised )


#		from PyQt5 import QtWidgets
#		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
#		sizePolicy.setHeightForWidth(self.separatorLine.sizePolicy().hasHeightForWidth())
#		self.separatorLine.setSizePolicy(sizePolicy)
#		self.separatorLine.setStyleSheet("font: 9pt;")
#		self.separatorLine.setLineWidth(0)
#		self.separatorLine.setMidLineWidth(10)
#		self.separatorLine.setGeometry(0, self.pixmap.height() + 130, self.pixmap.width(), 30)
		
#		print("Happy")

	def update_image(self):
		if(self.i < self.epochSlider.value()):
			self.action_button.setEnabled(False)
			self.contrast.fit(1)
			self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.contrast.data)))
			self.i += 1
		else:	
			self.timer.stop()
			self.action_button.setEnabled(True)
			self.run = True


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

