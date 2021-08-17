from PyQt5.QtCore import QThread, pyqtSignal
import cv2 as cv
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSlot

class Thread(QThread):
   change_pixmap = pyqtSignal(QImage)
   def run(self):
    cap = (cv.VideoCapture('rtsp://admin:admin@192.168.10.12:554/live/main'))
    while(True):
            ret, frame = cap.read()
            if ret:
                rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap.emit(p)
                
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()
        '''
        self.grid_layout = QGridLayout()
        self.screen_resolution = QApplication.desktop().availableGeometry()
        self.show_stream = QImage()
        '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # stylesheetfile = "dark-orange-green.qss"
    # with open(stylesheetfile,"r") as fh:
    #     app.setStyleSheet(fh.read())
    main = mainForm()
    main.showMaximized()
    ret = app.exec_()
    if main.edge_finder is not None:
        if main.edge_finder.isRunning():
            main.edge_finder.terminate()
    sys.exit(ret)