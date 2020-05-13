import time

import numpy as np
from PIL import Image
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QFileDialog, QErrorMessage, QMessageBox
from PyQt5.QtWidgets import QMainWindow

from gui.general import *
import os

class App(QMainWindow):
    """
    Standard application interface

    Parameters
    ----------
    image : ndarray
        The image to open
    """
    image: str
    title: str
    total_epochs: int
    epoch: int

    def __init__(self, image='./files/test_images/lena.png'):
        super().__init__()
        self.image = image
        self.title = os.path.basename(self.image)

        self.epoch = 0
        self.total_epochs = 0
        self.timer = QTimer(self)

    def get_available_windows(self, INFILE):
        """
        Get all the windows

        Parameters
        ----------
        INFILE : str
            Makes sure we don't reload the file recursively
        """
        global WINDOW_MANAGER
        return WINDOW_MANAGER.filter(INFILE)

    #   https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
    def center(self):
        """
        Center the window
        """
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())

    def epochs_change(self):
        """
        Updates the epoch label
        """
        epochs: int = self.epoch_slider.value()
        self.epoch_label.setText("Epochs ({}) (Total {})".format(epochs, self.total_epochs))

    def alpha_chnage(self):
        """
        update the method alpha value based on slider
        """
        value: int = self.alpha_slider.value()
        self.method.set_alpha(value / 100)
        self.alpha_label.setText("Alpha ({})".format(value / 100))

    def boundary_change(self):
        """
        Update the boundary based on the boundary group
        """
        if not self.boundary_group is None:
            self.method.set_boundary(self.boundary_group.checkedButton().text())

    def method_change(self):
        """
        Update the method based on the boundary group
        """
        if not self.method_group is None:
            self.method.set_mode(self.method_group.checkedButton().text())

    def mode_change(self, _):
        """
        Changes the view from the combobox
        """
        view = self.WINDOWS[self.mode.currentText()]
        view.init_UI()
        view.show()
        self.hide()

    @pyqtSlot()
    def update_image_label(self, data=None):
        """
        Update image label

        Parameters
        ----------
        data : ndarray
            The new image data
        """
        if data is None:
            self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))
        else:
            self.label.setPixmap(pil2pixmap(Image.fromarray((255 * data).astype(np.uint8))))

    @pyqtSlot()
    def update_image(self):
        """
        Wrapper to nicely update the image when preform a iteration from the backend
        """
        if not hasattr(self, 'epoch_slider'):
            QApplication.processEvents()
            self.method.fit(epochs=1)
            self.update_image_label()
            self.reset_button.setEnabled(True)
            self.timer.stop()
            QApplication.restoreOverrideCursor()
        else:
            if self.epoch < self.epoch_slider.value():
                self.method.fit(epochs=1)
                self.update_image_label()
                self.epoch += 1
                self.total_epochs += 1
                self.epochs_change()
                self.reset_button.setEnabled(True)
                QApplication.processEvents()
                self.setWindowTitle("Calculating...")
            else:
                QApplication.restoreOverrideCursor()
                self.setWindowTitle(self.title)
                self.reset_button.setEnabled(True)
                self.action_button.setEnabled(True)
                self.timer.stop()

    def show_file_dialog(self):
        """
        Shows a file dialog
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "JPEG (*.jpeg);;jpg (*.jpg);;png (*.png)",
                                                   options=options)
        if file_name:
            movment_x, movment_y = self.method.change_photo(file_name)
            self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))
            self.label.move(movment_x, self.label.pos().y())
        else:
            print("No file selected")

    def show_file_dialog_hdr(self):
        """
        Shows a file dialog
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                    "JPEG (*.jpeg);;jpg (*.jpg);;png (*.png)",
                                                    options=options)
        if file_name:
            if len(file_name) == 1:
                warning = QMessageBox()
                warning.setIcon(QMessageBox.Critical)
                warning.setText("Error")
                warning.setInformativeText('Use the shift key to select more photos (one photo = bad results)')
                warning.setWindowTitle("Error")
                warning.exec_()
            
            movment_x, movment_y = self.method.change_photo(file_name[0])
            self.method.update_images(file_name)
            self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))
            self.label.move(movment_x, self.label.pos().y())
        else:
            print("No file selected")

    def show_extra(self):
        """
        Shows the extra features
        """
        self.setGeometry(0, 0, self.pixmap.width() + self.PADDING, self.height)
        self.center()

    def screenshot(self):
        """
        Takes a screenshot of the current QWindow
        """
        screen = self.grab()
        screen.save("{}.png".format(time.time()), 'png')

    @pyqtSlot()
    def reset_image_extra(self):
        """
        Resets the image
        """
        self.total_epochs = 0
        if hasattr(self, 'epoch_label'):
            self.epoch_label.setText("Epochs")
        self.reset_button.setEnabled(False)
        self.method.reset()
        self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))

    def prepare(self):
        """
        Some functions needs some function to be run before method

        This method will be overridden
        """
        pass

    @pyqtSlot()
    def run_method(self, lock_run=False):
        """
        Runs one of the backends methods
        """
        self.prepare()
        if lock_run:
            QTimer.singleShot(100, lambda: self.action_button.setEnabled(False))
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents()
        self.epoch = 0
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)

    def undo(self):
        """
        Some functions needs some function to be run when the method is reset

        This method will be overridden
        """
        pass

    def reset_image(self):
        """
        Resets the image
        """
        if hasattr(self, 'epoch_label'):
            self.epoch_label.setText("Epochs")
        self.total_epochs = 0
        self.undo()
        self.reset_button.setEnabled(False)
        QTimer.singleShot(100, lambda: self.action_button.setEnabled(True))
        self.method.reset()
        self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))
