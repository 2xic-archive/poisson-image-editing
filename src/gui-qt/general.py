from PyQt5.QtGui import QIcon, QPixmap, QImage
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



"""
{ item_description }
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class fileExplorer(QWidget):
	def __init__(self):
		super().__init__()
	
	def initUI(self):
			
		self.file_explorer()		
		#self.show()
	
	def file_explorer(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;JPEG (*.jpeg);;jpg (*.jpg);;png (*.png)", options=options)
		if fileName:
			print(fileName)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = fileExplorer()
	window.initUI()
	window.close()
#	window.show()
#	sys.exit(app.exec_())
