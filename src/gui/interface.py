from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtWidgets import QPushButton, QSlider
from PyQt5.QtCore import Qt
#from general import *
from gui.app_data import *
from gui.general import pil2pixmap

class screen_element:
    def __init__(self, element):
        self.element = element
        self.height = None
        self.width = None
        self.x = 0
        self.y = -1

    def get_size_position(self):
        return self.element, (self.height, self.width), self.x, self.y


class interface_class(App):
    def __init__(self):
        App.__init__(self)
       # super().__init__()
        self.screen_elements = [

        ]
        self.screen_elements_id = {

        }
        self.padding = 30

    def update_geometry(self, height, width, element_id=None, x=0, y=-1):
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
        current_height = 30
        width_size = 0
        height_size = 0
        for index, obj_element in enumerate(self.screen_elements):
            element, size, pos_x, pos_y = obj_element.get_size_position()
            if not pos_y == -1:
                current_height = pos_y
            element.setGeometry(pos_x, current_height, element.width() if (size[0] == None) else size[0],
                                element.height() if (size[1] == None) else size[1])
            #	this is given to the window, we want to make sure everything fits
            width_size = max(element.width(), width_size)
            height_size = max(current_height, height_size)
            #	increasing the size so the next element comes after the current
            current_height += element.height() if (0 < index) else 0
        return width_size, height_size + self.padding

    def add_mode_switch(self, action, element_id):
        mode = QComboBox(self)
        mode.addItem("Change mode")
        for keys in self.get_avaible_windows(__file__):
            mode.addItem(keys)
        mode.currentIndexChanged.connect(action)

        element = screen_element(mode)
        self.screen_elements_id[element_id] = element
        self.screen_elements.append(element)
        return mode

    def add_image(self, data, parse):
        label = QLabel(self)
        pixmap = pil2pixmap(parse(data))
        label.setPixmap(pixmap)
        self.screen_elements.append(screen_element(label))
        return label, pixmap

    def first_upper(self, text):
        if 0 < len(text):
            text = list(text)
            text[0] = text[0].upper()
            text = "".join(text)
        return text

    def add_label(self, text):
        label = QLabel(self)
        label.setText(self.first_upper(text))
        self.screen_elements.append(screen_element(label))
        return label

    def add_slider(self, text, action):
        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(1)
        slider.setMaximum(10)
        slider.setSingleStep(1)
        if 0 < len(text):
            slider.setToolTip(text)
        slider.valueChanged.connect(action)
        self.screen_elements.append(screen_element(slider))
        return slider

    def add_button(self, text, action, setEnabled=True):
        action_button = QPushButton(text, self)
        action_button.clicked.connect(action)
        action_button.setEnabled(setEnabled)
        self.screen_elements.append(screen_element(action_button))
        return action_button
