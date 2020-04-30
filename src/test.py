
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QMainWindow, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import sys
from PyQt5.QtGui import QImage, QPixmap

class Button(QLabel):
  
    def __init__(self, title, parent, loc):
        super().__init__(title, parent)
        #label = QLabel(self)
        pixmap = QPixmap(loc)
        self.setPixmap(pixmap)

        print(pixmap)
        

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


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):
        self.setAcceptDrops(True)


       # button.move(100, 65)
        
        label = QLabel(self)
        pixmap = QPixmap('test.png')#'./files/test_images/source_v2.png')
        label.setPixmap(pixmap)

        #label.move(100, 65)

        #Stack = QVBoxLayout (self)
        #Stack.addWidget (label)
        #Stack.addWidget(button)

       # Stack.setGeometry(0, 0, 200, 200)
       # label.setGeometry(0, 0, 300, 300)

        self.button = Button('Button', self, './files/test_images/source_v2.png')
        self.button.setGeometry(0, 0, 30, 30)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)
        
    def dragEnterEvent(self, e):
        e.accept()
        
    def dropEvent(self, e):
        print(e)
        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()
        

if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_() 
