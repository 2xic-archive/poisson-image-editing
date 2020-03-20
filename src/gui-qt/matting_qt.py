#from PIL import Image
#from main import *
from general_window import *
import matting
#from general import pil2pixmap



class matting_window(general_window):
	def __init__(self, parent=None):	
		general_window.__init__(self, lambda x: Image.fromarray((x * 255).astype(np.uint8), mode = 'RGBA'))
		self.method = matting.matting(self.image)

	'''
	def initUI(self):
		self.setWindowTitle(self.title)

		"""
		Showing the image
		"""
		self.label = QLabel(self)

		#	TODO : Clean this up
		self.pixmap = pil2pixmap(Image.fromarray((self.matting.data * 255).astype(np.uint8), mode = 'RGBA'))
		self.label.setPixmap(self.pixmap)
		self.label.setGeometry(0, 30, self.pixmap.width(), self.pixmap.height());

		"""
		Showing the epoch count label
		"""
		self.epoch_label = QLabel(self)
		self.epoch_label.setText("Epochs")
		self.epoch_label.setGeometry(0, self.pixmap.height() + 30, self.pixmap.width(), 30)

		"""
		Showing the epoch slider
		"""		
		self.epochSlider = QSlider(Qt.Horizontal, self)
		self.epochSlider.setMinimum(1)
		self.epochSlider.setMaximum(10)
		self.epochSlider.setSingleStep(1)		
		self.epochSlider.setGeometry(0, self.pixmap.height() + 60, self.pixmap.width(), 30)
		self.epochSlider.setToolTip('How many epochs to run for?')
		self.epochSlider.valueChanged.connect(self.epochs_change)


		"""
		Showing the run button
		"""
		self.action_button = QPushButton('Run', self)
		self.action_button.move(self.action_button.frameGeometry().width() // 2, self.pixmap.height() + 90)
		self.action_button.clicked.connect(self.run_method)

		"""
		Showing the run reset
		"""
		self.reset_button = QPushButton('Reset', self)
		self.reset_button.move(self.reset_button.frameGeometry().width() // 2, self.pixmap.height() + 120)
		self.reset_button.clicked.connect(lambda x: QTimer.singleShot(100, lambda: self.reset_image()))
		self.reset_button.setEnabled(False)

		"""
		Showing the possible modes
		"""
		self.mode = QComboBox(self)
		self.mode.addItem("Change mode")
		for keys in self.get_avaible_windows(__file__):
			self.mode.addItem(keys)

		self.mode.setGeometry(0, 0, self.pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.mode_change)

		self.setGeometry(0, 0 , self.pixmap.width(), self.pixmap.height() + 150)
		self.center()
	'''

