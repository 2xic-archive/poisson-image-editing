import sys
from PyQt5.QtWidgets import QApplication
from gui.interfaces import blurring_qt

"""
main.py
====================================
The core module of the project
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = blurring_qt.blur_window()

    ex.init_UI()
    ex.show()
    sys.exit(app.exec_())
    print("running")
