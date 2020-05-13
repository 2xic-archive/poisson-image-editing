from PIL import Image
from PyQt5.QtCore import QTimer
# from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox

from gui.interface import interface_class


class general_window(interface_class):
    """
    Converts the input into a format QT likes

    Parameters
    ----------
    pixmap_converter : lambda
        Lambda function used to parse a image into QT
    load_extra : lambda
        Lambda function used to parse a load extra content
    """

    def __init__(self, pixmap_converter=None, load_extra=None, load_before=None):
        interface_class.__init__(self)
        self.pixmap_converter = pixmap_converter
        self.load_extra = load_extra
        self.load_before = load_before

    def init_UI(self):
        """
        initialize the UI
        """
        self.setWindowTitle(self.title)
        """
        Showing the possible modes
        """
        self.mode = self.add_mode_switch(action=self.mode_change, element_id="mode")

        """
        Showing the image
        """
        self.label, self.pixmap = self.add_image(self.method.data, (
            lambda x: self.pixmap_converter(x)) if not self.pixmap_converter is None else (
            lambda x: Image.fromarray(255 * x)), action=lambda x: self.save())
        self.update_geometry(self.pixmap.width(), self.pixmap.height(), y=30)
        self.update_geometry(self.pixmap.width(), 20, element_id="mode", y=5)

        """
        Make sure elements that should be loaded before is loaded
        """
        if not self.load_before is None:
            self.load_before()

        """
        Showing the boundary box options
        """
        self.boundary_group = None
        self.method_group = None

        self.boundary_box, self.boundary_group = self.add_radio_buttons("Boundary", [
            "Neumann", "Dirichlet"
        ], self.boundary_change, 0)
        self.update_geometry(self.boundary_box.width(), 90, x=10)

        """
        Showing the method box options
        """
        self.boundary_box, self.method_group = self.add_radio_buttons("Method", [
            "Explicit", "Implicit"
        ], self.method_change, 0, disabled_box=True)
        self.update_geometry(self.boundary_box.width(), 90, x=10 + self.boundary_box.width(), y=-42)

        """
        Showing the Alpha label
        """
        self.alpha_label = self.add_label("Alpha")
        self.update_geometry(self.pixmap.width(), 30, x=10)

        """
        Showing the epoch slider
        """
        self.alpha_slider = self.add_slider('Alpha', action=self.alpha_chnage, value=25)
        self.update_geometry(self.pixmap.width(), 30)
        self.alpha_chnage()

        """
        Showing the epoch count label
        """
        self.epoch_label = self.add_label("epochs")
        self.update_geometry(self.pixmap.width(), 30, x=10)

        """
        Showing the epoch slider
        """
        self.epoch_slider = self.add_slider('How many epochs to run for?', action=self.epochs_change)
        self.update_geometry(self.pixmap.width(), 30)

        """
        Showing the run button
        """
        self.action_button = self.add_button("Run", self.run_method)
        self.update_geometry(self.pixmap.width(), 30)

        """
        Showing the reset button
        """
        self.reset_button = self.add_button("Reset", lambda x: QTimer.singleShot(100, lambda: self.reset_image()),
                                            setEnabled=False)
        self.update_geometry(self.pixmap.width(), 30)

        """
        Showing the custom file button
        """
        self.open_button = self.add_button("Open", lambda x: QTimer.singleShot(100, lambda: self.show_file_dialog()),
                                           setEnabled=True)
        self.update_geometry(self.pixmap.width(), 30)

        if not self.load_extra is None:
            self.load_extra()

        """
        Position all the elements
        """
        width, height = self.position()
        self.setGeometry(0, 0, width, height)
        self.center()

    def save(self):
        """
        Saves the image
        """
        qm = QMessageBox
        ret = qm.question(self, '', "Are you sure to save the image?", qm.Yes | qm.No)
        if ret == qm.Yes:
            self.method.save(str(self.total_epochs) + "_" + self.title)
