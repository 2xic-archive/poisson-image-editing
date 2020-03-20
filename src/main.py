import os
import sys
sys.path.append("./gui/")
sys.path.append("./gui/interface/")
sys.path.append("./engine/")
sys.path.append("./backend/")
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from PIL import Image
import numpy as np
from PIL import Image
import os
from general import pil2pixmap
from PIL import Image
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget


class App(QMainWindow):
	def __init__(self, parrent=None, image='./files/test_images/lena.png'):
		super().__init__()
		self.image = image
		self.title = os.path.basename(self.image)
		self.left = 0
		self.top = 0

		self.epoch = 0
		self.total_epochs = 0
		self.timer = QTimer(self)

	def get_avaible_windows(self, INFILE):
		import blurring_qt as blur_window
		import inpaiting_qt as inpait_window
		import contrast_qt as contrast_window
		import demosaic_qt as demonsaic_window
		import matting_qt as matting_window
		import grayscale_qt as grayscale_window
		import anonymizing_qt as anonymizing_window

		self.WINDOWS = {

		}
		if (blur_window.__file__ not in INFILE):
			self.WINDOWS["Blurring"] = blur_window.blur_window()
		if (inpait_window.__file__ not in INFILE):
			self.WINDOWS["Inpaiting"] = inpait_window.inpait_window()
		if (contrast_window.__file__ not in INFILE):
			self.WINDOWS["Contrasting"] = contrast_window.contrast_window()
		if (demonsaic_window.__file__ not in INFILE):
			self.WINDOWS["Demonsaicing"] = demonsaic_window.demonsaic_window()
		if (matting_window.__file__ not in INFILE):
			self.WINDOWS["Matting"] = matting_window.matting_window()
		if (grayscale_window.__file__ not in INFILE):
			self.WINDOWS["Grayscale"] = grayscale_window.grayscale_window()
		if (anonymizing_window.__file__ not in INFILE):
			self.WINDOWS["Anoymousing"] = anonymizing_window.anonymous_window()
		return self.WINDOWS

	#	https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def epochs_change(self):
		epochs = self.epochSlider.value()
		self.epoch_label.setText("Epochs ({}) (Total {})".format(epochs, self.total_epochs))

	def mode_change(self, _):
		view = self.WINDOWS[self.mode.currentText()]
		view.initUI()
		view.show()
		self.hide()

	def update_image(self):
		if(self.epoch < self.epochSlider.value()):
			self.method.fit(epochs=1)
			self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))
			self.epoch += 1
			self.total_epochs += 1
			self.epochs_change()
		else:	
			self.reset_button.setEnabled(True)
			self.timer.stop()

	def show_file_dialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;JPEG (*.jpeg);;jpg (*.jpg);;png (*.png)", options=options)
		if fileName:
			"""
			TODO : Add custom files
			Should not be 2 hard, however we have to figure how the image should be displayed as QT else will crash
			"""
			#self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))
			raise Exception("Feature is not fully implemented (yet)")

	def show_extra(self):
		self.setGeometry(0, 0 , self.pixmap.width() + self.PADDING, self.height)
		self.center()

	@pyqtSlot()
	def reset_image_extra(self):
		self.total_epochs = 0
		self.reset_button.setEnabled(False)
		self.method.reset()
		self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))

	@pyqtSlot()
	def run_method(self):
		self.epoch = 0
		self.timer.timeout.connect(self.update_image)
		self.timer.start(100)

if __name__ == '__main__':
	from blurring_qt import blur_window
	app = QApplication(sys.argv)
	ex = blur_window()
	ex.initUI()
	ex.show()
	sys.exit(app.exec_())

