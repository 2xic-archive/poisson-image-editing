from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtWidgets import QPushButton, QSlider, QGridLayout
from PyQt5.QtWidgets import QCheckBox, QGroupBox, QButtonGroup, QVBoxLayout, QRadioButton
from PyQt5.QtCore import Qt
from gui.app_data import *
from gui.general import pil2pixmap
from typing import Callable
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import sys
from PyQt5.QtGui import QImage, QPixmap
from gui.window_manager import *

WINDOW_MANAGER = window()

class draggable_style(QLabel):  
    def __init__(self, title, parent, loc):
        super().__init__(title, parent)
        #label = QLabel(self)
        self.pixmap = QPixmap(loc)
        self.setPixmap(self.pixmap)
        #self.size = loc.shape
        #print(pixmap)
        

    def mouseMoveEvent(self, e):
        print("???")

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()
        print("???")

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')

class screen_element:
	"""
	This class describes a screen element.
	"""
	def __init__(self, element, free_floating=False):
		self.element = element
		self.height = None
		self.width = None
		self.x = 0
		self.y = -1
		self.index_id = 0
		self.free_floating = free_floating
		self.size_element = element

	def get_size_position(self):
		"""
		Gets the size position.
		"""
		return self.element, (self.height, self.width), self.x, self.y


class interface_class(App):
	"""
	A more abstract way to make a QT window
	"""
	def __init__(self):
		App.__init__(self)
		self.screen_elements = [

		]
		self.screen_elements_id = {

		}
		self.padding = 30

	def update_geometry(self, height: int, width: int, element_id: str=None, x: int =0, y:int =-1):
		"""
		Update the geometry

		of the last image or one specified

		Parameters
		----------
		heigth : int
			set the height of a image
		width : int
			set the width of a image
		element_id : str
			the element_id to check against
		x : int
			sets the x position
		y : int
			sets the y position        
		"""
		if element_id is None:
			self.screen_elements[-1].height = height
			self.screen_elements[-1].width = width
			self.screen_elements[-1].x = x
			self.screen_elements[-1].y = y
		else:
			self.screen_elements_id[element_id].height = height
			self.screen_elements_id[element_id].width = width
			self.screen_elements_id[element_id].x = x
			self.screen_elements_id[element_id].y = y

	def position(self):
		"""
		Returns
		-------
		int
			the max width of a element
		int
			the highest a element is positioned
		"""
		current_height = 30
		width_size = 0
		height_size = 0
		for index, obj_element in enumerate(self.screen_elements):
			if obj_element.free_floating:
				obj_element.element.setGeometry(0, 30, obj_element.size_element.width(), obj_element.size_element.height())
				continue
			element, size, pos_x, pos_y = obj_element.get_size_position()
			if not pos_y == -1 and not pos_y == -42:
				current_height = pos_y
			element.setGeometry(pos_x, current_height, element.width() if (size[0] == None) else size[0],
								element.height() if (size[1] == None) else size[1])
			#	this is given to the window, we want to make sure everything fits
			width_size = max(element.width(), width_size)
			height_size = max(current_height, height_size)
			#	increasing the size so the next element comes after the current
			if (index + 1) < len(self.screen_elements) and self.screen_elements[index + 1].y == -42:
				#current_height += element.height() if (0 < index) else 0
				pass
			else:
				current_height += element.height() if (0 < index) else 0

		return width_size, height_size + self.padding

	def add_mode_switch(self, action, element_id):
		"""
		Creates a QComoBox with all the windows

		Parameters
		----------
		action : lambda
			the action to run on change of index
		element_id : str
			a id given to the element
		Returns
		-------
		QComboBox
			a QComboBox with all the windows
		"""
		mode = QComboBox(self)
		mode.addItem("Change mode")

		global WINDOW_MANAGER
		WINDOW_MANAGER.build()
		self.WINDOWS = WINDOW_MANAGER.filter(__file__)
		for keys in self.WINDOWS:
			mode.addItem(keys)

		mode.currentIndexChanged.connect(action)

		element = screen_element(mode)
		self.screen_elements_id[element_id] = element
		self.screen_elements.append(element)
		return mode

	def add_image(self, data, parse, action=None):
		"""
		Creates a QLabel with a image

		Parameters
		----------
		data : ndarray
			the image
		parse : lambda
			a function used to parse the image to a QT compatible format
		Returns
		-------
		QLabel
			the QLabel with a image
		QPixmap
			the pixmap of the image
		"""
		label = QLabel(self)
		pixmap = pil2pixmap(parse(data))
		label.setPixmap(pixmap)
		if not action is None:
			label.mousePressEvent = action
		self.screen_elements.append(screen_element(label))
		return label, pixmap

	def add_image_draggable(self, data, parse, parrent):
		"""
		Creates a QLabel with a image

		Parameters
		----------
		data : ndarray
			the image
		parse : lambda
			a function used to parse the image to a QT compatible format
		Returns
		-------
		QLabel
			the QLabel with a image
		QPixmap
			the pixmap of the image
		"""
		label = draggable_style("", parrent, pil2pixmap(parse(data)))
		#pixmap = pil2pixmap(parse(data))
		#label.setPixmap(pixmap)
		screen_el = screen_element(label, free_floating=True)
		screen_el.size_element = label.pixmap
		self.screen_elements.append(screen_el)
		return label, None

	def first_upper(self, text):
		"""
		Makes the first letter uppercase

		Parameters
		----------
		text : str
			the string to make uppercase
		
		Returns
		-------
		str
			string with the first case uppercase
		"""
		if 0 < len(text):
			text = list(text)
			text[0] = text[0].upper()
			text = "".join(text)
		return text

	def add_label(self, text):
		"""
		Creates a QLabel 

		Parameters
		----------
		text : str
			set the QLabel string

		Returns
		-------
		QLabel
			the QLabel with the text
		"""
		label = QLabel(self)
		label.setText(self.first_upper(text))
		self.screen_elements.append(screen_element(label))
		return label

	def add_slider(self, text, action: Callable, value: int = -1):
		"""
		Creates a QSlider 

		Parameters
		----------
		text : str
			set the QSlider tool tip
		action : lambda
			set the button action
		Returns
		-------
		QSlider
			the QSlider with tool tip
		"""
		slider = QSlider(Qt.Horizontal, self)
		slider.setMinimum(1)
		slider.setMaximum(10)
		slider.setSingleStep(1)
		if 0 < len(text):
			slider.setToolTip(text)
		if 0 < value:
			slider.setValue(value)
		slider.valueChanged.connect(action)
		self.screen_elements.append(screen_element(slider))
		return slider

	def add_checkbox(self, text, action: Callable):
		box = QCheckBox(text, self)
		box.stateChanged.connect(action)

		self.screen_elements.append(screen_element(box))
		return box

	def add_button(self, text, action, setEnabled=True):
		"""
		Creates a QPushButton 

		Parameters
		----------
		text : str
			set the QPushButton text
		action : lambda
			set action of the QPushButton 
		setEnabled: bool
			if should the button be enabled from start
		Returns
		-------
		QPushButton
			the QPushButton with the given action 
		"""
		action_button = QPushButton(text, self)
		action_button.clicked.connect(action)
		action_button.setEnabled(setEnabled)
		self.screen_elements.append(screen_element(action_button))
		return action_button

	def add_radio_buttons(self, text, button_text, action, enabled):
		"""
		Creates a QPushButton 

		Parameters
		----------
		text : str
			a string describing the box
		button_text : list
			a list of button text
		action : lambda
			the action to run when a new button is toggeled
		enabled: int
			the button index to have enabled from the start
		Returns
		-------
		QGroupBox
			a QGroupBox with the given buttons
		"""
		box = QGroupBox(text, self)
		mood_button_group = QButtonGroup()
		button_layout = QVBoxLayout()
		for index, i in enumerate(button_text):
			i = QRadioButton(i)
			button_layout.addWidget(i)
			if not action is None:
				i.toggled.connect(action)
			mood_button_group.addButton(i, index)
			if index == enabled:
				i.setChecked(True)
			print(i)
		box.setLayout(button_layout)

		self.screen_elements.append(screen_element(box))
		return box, mood_button_group

	def add_input_group(self, text, button_text, action, enabled):
		box = QGroupBox(text, self)
		mood_button_group = []
		button_layout = QVBoxLayout()
		for index, text in enumerate(button_text):
			i = QLineEdit()
			i.setPlaceholderText(text) 
			i.textChanged.connect(action[index])
			button_layout.addWidget(i)
			mood_button_group.append(i)
		#	if not action is None:
		#		i.toggled.connect(action)
			#mood_button_group.addWidget(i)#, index)
			#if index == enabled:
			#	i.setChecked(True)
			print(i)
		box.setLayout(button_layout)

		self.screen_elements.append(screen_element(box))
		return box, mood_button_group		

	def add_input_button(self, text, button_text, action, enabled):
		box = QGroupBox(text, self)
		mood_button_group = []
		button_layout = QVBoxLayout()
		for index, text in enumerate(button_text):
			i = QPushButton(text)
#			i.setPlaceholderText(text) 
			i.clicked.connect(action[index])
			button_layout.addWidget(i)
			mood_button_group.append(i)
		#	if not action is None:
		#		i.toggled.connect(action)
			#mood_button_group.addWidget(i)#, index)
			#if index == enabled:
			#	i.setChecked(True)
			print(i)
		box.setLayout(button_layout)

		self.screen_elements.append(screen_element(box))
		return box, mood_button_group		





