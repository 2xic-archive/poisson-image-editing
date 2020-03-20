from main import *
from extra.local_adaptive_histogram import *
import contrasting
from general_window import general_window

class contrast_window(general_window):
	def __init__(self, parent=None):	
		general_window.__init__(self, load_extra=lambda x: self.load_extra_now())
		self.image = '../test_images/contrast.jpg'
		self.method = contrasting.contrast(self.image)
		self.input_image = self.method.get_data().copy()
		self.height = 0
#		self.initUI()	
#		self.load_extra_now()
#		self.loaded = False

	def load_extra_now(self):
#		if not self.loaded:
#			self.loaded = True
#			self.initUI()
#			print(self.label)
#			print("???")
		"""
		Load the extra
		"""

		_, self.heigth = self.position()
		self.extra_button = self.add_button("Extra", lambda x: QTimer.singleShot(100, lambda: self.show_extra()))
		self.update_geometry(self.pixmap.width(), 30)			
		self.reset_heigth()


		self.PADDING = self.pixmap.width() + 30

		self.extra_label, self.extra_pixmap = self.add_image(self.method.data, (lambda x : self.pixmap_converter(x)) if not self.pixmap_converter is None else (lambda x: Image.fromarray(255 * x)))
		self.update_geometry(self.pixmap.width(), self.pixmap.height(), x=self.PADDING, y=self.label.pos().y())

		self.extra_action_button = self.add_button("Local adaptive histogram", lambda x: QTimer.singleShot(100, lambda: self.update_image_histogram()))
		self.update_geometry(self.pixmap.width(), 30, x=self.PADDING, y=self.action_button.pos().y())			
		#QPushButton('Local adaptive histogram', self)
#		self.extra_action_button.setMinimumWidth(180)

#		self.extra_action_button.move(self.PADDING , self.action_button.pos().y())
#		self.extra_action_button.clicked.connect(lambda x: QTimer.singleShot(100, lambda: self.update_image_histogram()))

#		self.	

	#	self.extra_label = QLabel(self)
	#	self.extra_pixmap = pil2pixmap(Image.fromarray(255 * self.contrast.data))
	#	self.extra_label.setPixmap(self.pixmap)
	#	self.extra_label.setGeometry(self.PADDING, 30, self.extra_pixmap.width(), self.extra_pixmap.height());


#		App.__init__(self)
#		self.image = '../test_images/contrast.jpg'
#		self.title = self.image
#		self.contrast = contrasting.contrast(self.image)
#		self.input_image = self.contrast.get_data().copy()
#		self.method = self.contrast



	'''
	def initUI(self):
		self.setWindowTitle(self.title)
		"""
		Showing the image
		"""
		self.label = QLabel(self)
		self.pixmap = pil2pixmap(Image.fromarray(255 * self.contrast.data))
		self.label.setPixmap(self.pixmap)
		self.label.setGeometry(0, 30, self.pixmap.width(), self.pixmap.height());

		"""
		Showing the epoch label
		"""
		self.epoch_label = QLabel(self)
		self.epoch_label.setText("Epochs")
		self.epoch_label.setGeometry(0, self.pixmap.height() + 110, self.pixmap.width(), 30)
		
		"""
		Showing the epch slider
		"""
		self.epochSlider = QSlider(Qt.Horizontal, self)
		self.epochSlider.setMinimum(1)
		self.epochSlider.setMaximum(10)
		self.epochSlider.setSingleStep(1)		
		self.epochSlider.setGeometry(0, self.pixmap.height() + 140, self.pixmap.width(), 30)
		self.epochSlider.setToolTip('How many epochs to run for?')
		self.epochSlider.valueChanged.connect(self.epochs_change)

		"""
		Showing the button
		"""
		self.action_button = QPushButton('Run', self)
		self.action_button.move(self.action_button.frameGeometry().width(), self.pixmap.height() + 160)
		self.action_button.clicked.connect(self.run_method)

		"""
		Showing the reset
		"""
		self.reset_button = QPushButton('Reset', self)
		self.reset_button.move(0, self.pixmap.height() + 160)
		self.reset_button.clicked.connect(lambda x: QTimer.singleShot(100, lambda: self.reset_image()))
		self.reset_button.setEnabled(False)

		"""
		Showing the modes
		"""
		self.mode = QComboBox(self)
		self.mode.addItem("Change mode")
		for keys in self.get_avaible_windows(__file__):
			self.mode.addItem(keys)

		self.mode.setGeometry(0, 0, self.pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.mode_change)

		"""
			TODO : Chck if you can add this element later in the launch
				NOTE: adding a timer does not resolve the problem
		"""
		self.extra_button = QPushButton('Extra', self)
		self.extra_button.move(self.extra_button.frameGeometry().width() // 2, self.pixmap.height() + 85)
		self.extra_button.clicked.connect(self.show_extra)

		self.PADDING = self.pixmap.width() + 30
		self.extra_label = QLabel(self)
		self.extra_pixmap = pil2pixmap(Image.fromarray(255 * self.contrast.data))
		self.extra_label.setPixmap(self.pixmap)
		self.extra_label.setGeometry(self.PADDING, 30, self.extra_pixmap.width(), self.extra_pixmap.height());

		self.action_button = QPushButton('Local adaptive histogram', self)
		self.action_button.setMinimumWidth(180)
#		self.action_button.setWidth(120)
#		self.action_button.setGeometry(self.PADDING + self.action_button.frameGeometry().width() // 2, self.pixmap.height() + 160, self.pixmap.width(), 30)
		self.action_button.move(self.PADDING , self.pixmap.height() + 160)
		self.action_button.clicked.connect(lambda x: QTimer.singleShot(100, lambda: self.update_image_histogram()))
		
		self.setGeometry(0, 0 , self.pixmap.width(), self.pixmap.height() + 200)
		self.center()
	'''

	def update_image_histogram(self):
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * contrast_enhancment(self.input_image))))

	def show_extra(self):
		print("WE OUT HERE???")
		self.setGeometry(0, 0 , self.pixmap.width() + self.PADDING, self.heigth)
		self.center()

