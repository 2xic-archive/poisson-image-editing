import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider
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


#from : 	
#	https://stackoverflow.com/questions/28086613/pillow-pil-to-qimage-conversion-python-exe-has-stopped-working
#	https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue
def pil2pixmap(im):
	if im.mode == "RGB":
		pass
	elif im.mode == "L":
		im = im.convert("RGBA")
	data = im.convert("RGBA").tobytes()
	qim = QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)
	pixmap = QPixmap.fromImage(qim)
	return pixmap

class App(QWidget):

	def __init__(self):
		super().__init__()
		self.image = '../test_images/lena.png'
		self.title = self.image
		self.left = 0
		self.top = 0
		self.width = 640
		self.height = 480

		self.blak = blurring.blur(self.image)

		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)


		self.label = QLabel(self)
		pixmap = pil2pixmap(Image.fromarray(255 * self.blak.data))
		self.label.setPixmap(pixmap)
		self.resize(pixmap.width(), pixmap.height() + 100)
		self.move(0, 30)

		self.epoch_label = QLabel(self)
		self.epoch_label.setText("Epochs")
		self.epoch_label.setGeometry(0, pixmap.height() + 10, pixmap.width(), 30)

		self.epochSlider = QSlider(Qt.Horizontal, self)
		self.epochSlider.setMinimum(1)
		self.epochSlider.setMaximum(10)
		self.epochSlider.setSingleStep(1)
		
		self.epochSlider.setGeometry(0, pixmap.height() + 35, pixmap.width(), 30)
		self.epochSlider.setToolTip('How many epochs to run for?')
		self.epochSlider.valueChanged.connect(self.epochsChange)

		self.action_button = QPushButton('Run', self)
		self.action_button.move(self.action_button.frameGeometry().width() // 2, pixmap.height() + 70)
		self.action_button.clicked.connect(self.on_click)


		self.mode = QComboBox(self)
		self.mode.addItem("blurring")
		self.mode.addItem("inpait")
		self.mode.setGeometry(0, 0, pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.modeChange)

		self.timer = QTimer(self)
		self.i = 0

		self.show()
		self.center()

	#	https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def update_image(self):
		if(self.i < self.epochSlider.value()):
			self.action_button.setEnabled(False)
			self.blak.fit(1)
			self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.blak.data)))
			self.i += 1
		else:	
			self.timer.stop()
			self.action_button.setEnabled(True)
	"""
	informing the user
	"""
	def epochsChange(self):
		size = self.epochSlider.value()
		self.epoch_label.setText("Epochs ({})".format(size))

	def modeChange(self, i):
		print(i)
		
	@pyqtSlot()
	def on_click(self):
		self.timer.timeout.connect(self.update_image)
		self.timer.start(100)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

