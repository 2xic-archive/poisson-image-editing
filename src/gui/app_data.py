from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QFileDialog

from gui.general import *
from PIL import Image
from gui import interface

import time

class App(QMainWindow):
    """
    Standard application interface

    Parameters
    ----------
    image : ndarray
        The image to open
    """
    def __init__(self, image=get_path(__file__) + '../files/test_images/lena.png'):
        super().__init__()
        self.image = image
        self.title = os.path.basename(self.image)
        self.left = 0
        self.top = 0

        self.epoch = 0
        self.total_epochs = 0
        self.timer = QTimer(self)

    def get_avaible_windows(self, INFILE):
        """
        Get all the windows

        Parameters
        ----------
        INFILE : str
            Makes sure we don't reload the file recursively
        """
        import gui.interfaces.blurring_qt as blur_window
        import gui.interfaces.inpaiting_qt as inpait_window
        import gui.interfaces.contrast_qt as contrast_window
        import gui.interfaces.demosaic_qt as demonsaic_window
        import gui.interfaces.matting_qt as matting_window
        import gui.interfaces.grayscale_qt as grayscale_window
        import gui.interfaces.anonymizing_qt as anonymizing_window
        import gui.interfaces.hdr_qt as hdr_window
        import gui.interfaces.non_edge_blurring_qt as non_edge_blurring
        self.WINDOWS = {

        }
        if blur_window.__file__ not in INFILE:
            self.WINDOWS["Blurring"] = blur_window.blur_window()
        if inpait_window.__file__ not in INFILE:
            self.WINDOWS["Inpainting"] = inpait_window.inpait_window()
        if contrast_window.__file__ not in INFILE:
            self.WINDOWS["Contrasting"] = contrast_window.contrast_window()
        if demonsaic_window.__file__ not in INFILE:
            self.WINDOWS["Demosaicing"] = demonsaic_window.demonsaic_window()
        if matting_window.__file__ not in INFILE:
            self.WINDOWS["Matting"] = matting_window.matting_window()
        if grayscale_window.__file__ not in INFILE:
            self.WINDOWS["Grayscale"] = grayscale_window.grayscale_window()
        if anonymizing_window.__file__ not in INFILE:
            self.WINDOWS["Anonymous"] = anonymizing_window.anonymizing_window()
        if anonymizing_window.__file__ not in INFILE:
            self.WINDOWS["Edge preserving blur"] = anonymizing_window.anonymizing_window()
        if non_edge_blurring.__file__ not in INFILE:
            self.WINDOWS["Edge preserving blur"] = non_edge_blurring.non_edge_blurring_window()
        if non_edge_blurring.__file__ not in INFILE:
            self.WINDOWS["HDR"] = hdr_window.hdr_window()
        return self.WINDOWS

    #   https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
    def center(self):
        """
        Center the window

        """       
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def epochs_change(self):
        """
        Updates the epoch label
        """
        epochs = self.epochSlider.value()
        self.epoch_label.setText("Epochs ({}) (Total {})".format(epochs, self.total_epochs))

    def mode_change(self, _):
        """
        Changes the view from the combobox
        """
        view = self.WINDOWS[self.mode.currentText()]
        view.init_UI()
        view.show()
        self.hide()

    def update_image(self):
        """
        Wrapper to nicely update the image when preform a iteration from the backend
        """
        if self.epoch < self.epochSlider.value():
            self.method.fit(epochs=1)
            self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))
            self.epoch += 1
            self.total_epochs += 1
            self.epochs_change()
            self.reset_button.setEnabled(True)
        else:
            self.reset_button.setEnabled(True)
            self.timer.stop()

    def show_file_dialog(self):
        """
        Shows a file dialog
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPEG (*.jpeg);;jpg (*.jpg);;png (*.png)",
                                                  options=options)
        if fileName:
            """
            TODO : Add custom files
            Should not be 2 hard, however we have to figure how the image should be displayed as QT else will crash
            """
            # self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))
            raise Exception("Feature is not fully implemented (yet)")

    def show_extra(self):
        """
        Shows the extra features
        """
        self.setGeometry(0, 0, self.pixmap.width() + self.PADDING, self.height)
        self.center()

    def sceenshot(self):
        p =  self.grab()
        p.save("{}.png".format(time.time()), 'png')

    @pyqtSlot()
    def reset_image_extra(self):
        """
        Resets the image
        """
        self.total_epochs = 0
        self.reset_button.setEnabled(False)
        self.method.reset()
        self.label.setPixmap(pil2pixmap(self.pixmap_converter(self.method.data)))

    @pyqtSlot()
    def run_method(self):
        """
        Runs one of the backends methods
        """
        self.epoch = 0
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)

    def reset_image(self):
        self.total_epochs = 0
        self.reset_button.setEnabled(False)
        self.method.reset()
        self.label.setPixmap(pil2pixmap(Image.fromarray((255 * self.method.data).astype(np.uint8))))


