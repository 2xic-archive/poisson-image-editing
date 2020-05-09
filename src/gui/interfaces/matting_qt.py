from backend import matting
from gui.general_window import *
import re
from PyQt5.QtCore import Qt, QMimeData

"""
class Button(QLabel):
  
    def __init__(self, title, parent):
        super().__init__(title, parent)
        #label = QLabel(self)
        pixmap = QPixmap('test.png')
        self.setPixmap(pixmap)

        print(pixmap)
        

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()


        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')
"""

class matting_window(general_window):
	"""
	This class describes a matting window.
	"""
	def __init__(self, parent=None):
		general_window.__init__(self, lambda x: Image.fromarray((x * 255).astype(np.uint8)), load_before=lambda x: self.load_extra_now())#, mode='RGBA'))
		self.method = matting.matting()#self.image)

	def get_int(self, field):
		response = re.findall(r'\d+', field)
		if(len(response) == 0):
			return None
		return int(response[0])

	def load_extra_now(self):
		"""
		Showing the image
		"""
		self.setAcceptDrops(True)
		self.label_, self.pixmap_ = self.add_image_draggable(self.method.source.data, (
			lambda x: self.pixmap_converter(x)) if not self.pixmap_converter is None else (
			lambda x: Image.fromarray(255 * x)), self)


		self.boundary_box, self.boundary_group_iamge_end = self.add_input_group("Crop location input", [
				"x", "y"
			], 
			[
				lambda x: QTimer.singleShot(100, lambda: self.update_image_size()),
				lambda x: QTimer.singleShot(100, lambda: self.update_image_size())
			], 0)
		self.update_geometry(self.boundary_box.width(), 90, x=10)

		self.boundary_box_max, self.boundary_group_iamge = self.add_input_group("SCrop location input", [
				"x1", "y1"
			], [
				lambda x: QTimer.singleShot(100, lambda: self.update_image_size()),
				lambda x: QTimer.singleShot(100, lambda: self.update_image_size())
			], 0)
		self.update_geometry(self.boundary_box_max.width(), 90, x=10 + self.boundary_box.width(), y=-42)


		def update_func():
			try:
				self.update_image_label(self.method.preview_box(*list(map(lambda x: self.get_int(x.text()), self.boundary_group_iamge_end + self.boundary_group_iamge))))
			except Exception as e:
				print(e)
		self.update_image_size()

	def update_image_size(self):
		"""
		Update the image size based on the input siz
		"""
		x0, y0, x1, y1 = list(map(lambda x: self.get_int(x.text()), self.boundary_group_iamge_end + self.boundary_group_iamge))
		if x0 == None:
			x0 = 0
		if y0 == None:
			y0 = 0
		if x1 == None:
			x1 = self.method.source.data.shape[1]
		if y1 == None:
			y1 = self.method.source.data.shape[0]
		if x0 < x1 and y0 < y1:
			self.area = [[x0, x1], [y0, y1]]
			self.label_.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.source.data[y0:y1, x0:x1]).astype(np.uint8))))   
		else:
			print("Feil størelse")

	def prepare(self):
		"""
		Prepare the method before run
		"""
		self.method.working_area = self.area
		self.method.padding = [self.label_.pos().x(), self.label_.pos().y()]
		self.label_.setVisible(False)

	def undo(self):
		self.label_.setVisible(True)

	def dragEnterEvent(self, e):
		"""
		Drag event handler for the source image

		Parameters
		----------
		e : QDragEnterEvent
			The drag event
		"""
		e.accept()
		
	def dropEvent(self, e):
		"""
		Drop event handler for the source image

		Parameters
		----------
		e : QDropEvent
			The drop event
		"""
		print(type(e))
		position = e.pos()
		self.label_.move(position)

		e.setDropAction(Qt.MoveAction)
		e.accept()




