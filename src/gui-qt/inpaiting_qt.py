from main import *
import inpaiting
from extra.median_filter import median_filter

class inpait_window(App):
	def __init__(self, parent=None):	
		App.__init__(self)
		self.inpait = inpaiting.inpait(self.image)
		self.method = self.inpait

	def initUI(self):
		self.setWindowTitle(self.title)

		"""
			Showing the image
		"""
		self.label = QLabel(self)
		self.pixmap = pil2pixmap(Image.fromarray(255 * self.inpait.data))
		self.label.setPixmap(self.pixmap)
		self.label.setGeometry(0, 30, self.pixmap.width(), self.pixmap.height());

		"""
			Showing the noise label
		"""
		self.noise_label = QLabel(self)
		self.noise_label.setText("Remove information")
		self.noise_label.setGeometry(0, self.pixmap.height() + 30, self.pixmap.width(), 30)

		"""
			Showing the noise slider
		"""
		self.noiseSlider = QSlider(Qt.Horizontal, self)
		self.noiseSlider.setMinimum(1)
		self.noiseSlider.setMaximum(10)
		self.noiseSlider.setSingleStep(1)
		self.noiseSlider.setGeometry(0, self.pixmap.height() + 60, self.pixmap.width(), 30)
		self.noiseSlider.setToolTip('How much information to remove?')


		"""
			Showing the noise button
		"""
		self.noise_button = QPushButton('Remove', self)
		self.noise_button.move(0, self.pixmap.height() + 85)
		self.noise_button.clicked.connect(lambda x: QTimer.singleShot(100, lambda: self.update_image_noise()))#self.action_add_noise)


		"""
			Showing the epoch label
		"""
		self.epoch_label = QLabel(self)
		self.epoch_label.setText("Epochs")
		self.epoch_label.setGeometry(0, self.pixmap.height() + 110, self.pixmap.width(), 30)


		"""
			Showing the epoch slider
		"""
		self.epochSlider = QSlider(Qt.Horizontal, self)
		self.epochSlider.setMinimum(1)
		self.epochSlider.setMaximum(10)
		self.epochSlider.setSingleStep(1)		
		self.epochSlider.setGeometry(0, self.pixmap.height() + 140, self.pixmap.width(), 30)
		self.epochSlider.setToolTip('How many epochs to run for?')
		self.epochSlider.valueChanged.connect(self.epochs_change)

		"""
			Showing the action button
		"""
		self.action_button = QPushButton('Run', self)
		self.action_button.move(self.action_button.frameGeometry().width(), self.pixmap.height() + 160)
		self.action_button.clicked.connect(self.run_method)
		self.action_button.setEnabled(False)

		"""
			Showing the reset button
		"""
		self.reset_button = QPushButton('Reset', self)
		self.reset_button.move(0, self.pixmap.height() + 160)
		self.reset_button.clicked.connect(lambda x: QTimer.singleShot(100, lambda: self.reset_image()))
		self.reset_button.setEnabled(False)

		"""
			Showing the modes button
		"""
		self.mode = QComboBox(self)
		self.mode.addItem("Change mode")
		for keys in self.get_avaible_windows(__file__):
			self.mode.addItem(keys)
		self.mode.setGeometry(0, 0, self.pixmap.width(), 30)
		self.mode.currentIndexChanged.connect(self.mode_change)

		"""
			TODO : Chck if you can add this element later in the launch
		"""
		self.extra_button = QPushButton('Extra', self)
		self.extra_button.move(self.extra_button.frameGeometry().width(), self.pixmap.height() + 85)
		self.extra_button.clicked.connect(self.show_extra)

		self.PADDING = self.pixmap.width() + 30
		self.extra_label = QLabel(self)
		self.extra_pixmap = pil2pixmap(Image.fromarray(255 * self.inpait.data))
		self.extra_label.setPixmap(self.pixmap)
		self.extra_label.setGeometry(self.PADDING, 30, self.extra_pixmap.width(), self.extra_pixmap.height());

		self.extra_action_button = QPushButton('Median filter', self)
		self.extra_action_button.move(self.PADDING + self.extra_action_button.frameGeometry().width() // 2, self.pixmap.height() + 160)
		self.extra_action_button.clicked.connect(lambda x : QTimer.singleShot(100, lambda: self.update_median()))
		self.extra_action_button.setEnabled(False)

		self.setGeometry(0, 0 , self.pixmap.width(), self.pixmap.height() + 200)
		self.center()

	def show_extra(self):
		self.setGeometry(0, 0 , self.pixmap.width() + self.PADDING, self.pixmap.height() + 200)
		self.center()

	def update_median(self):
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * median_filter(self.input_image))))
		
	def epochs_change(self):
		size = self.epochSlider.value()
		self.epoch_label.setText("Epochs ({})".format(size))

	@pyqtSlot()
	def reset_image(self):
		self.reset_button.setEnabled(False)
		self.action_button.setEnabled(False)
		self.noise_button.setEnabled(True)
		self.method.reset()
		self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.method.data)))

	def update_image_noise(self):
		self.inpait.destroy_information(self.noiseSlider.value())		
		self.extra_label.setPixmap(pil2pixmap(Image.fromarray(255 * self.inpait.data)))
		self.label.setPixmap(pil2pixmap(Image.fromarray(255 * self.inpait.data)))

		self.input_image = self.inpait.get_data().copy()

		self.extra_action_button.setEnabled(True)
		self.action_button.setEnabled(True)
		self.noise_button.setEnabled(False)
		self.reset_button.setEnabled(True)
