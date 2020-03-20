import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtGui import QImage, QPixmap
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