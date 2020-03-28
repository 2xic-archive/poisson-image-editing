"""
main.py
====================================
The core module of the project
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.interfaces import blurring_qt

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    ex = blurring_qt.blur_window()

    ex.init_UI()
    ex.show()
    sys.exit(APP.exec_())
    print("running")
