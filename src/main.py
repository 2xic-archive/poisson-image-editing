import sys

#sys.path.append("./gui/")
#sys.path.append("./gui/interface/")
#sys.path.append("./engine/")
#sys.path.append("./backend/")
from backend.blurring import *
#from gui.interface import *
from gui import *
from engine import *
from backend import *
from gui.general import pil2pixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QFileDialog

if __name__ == '__main__':
    from gui.interfaces.blurring_qt import blur_window
    app = QApplication(sys.argv)
    ex = blur_window()
    ex.init_UI()
    ex.show()
    sys.exit(app.exec_())
    print("running")