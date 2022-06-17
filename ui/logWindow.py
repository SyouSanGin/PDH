from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from cv2 import log
from ui_logWindow import Ui_logWindow

class LogWindow(QWidget):

    log = []
    redraw = False
    __counter = 0
    def __init__(self, par: QMainWindow):
        super(LogWindow,self).__init__(parent=par)
        self.par = par
        self.ui = Ui_logWindow()
        self.ui.setupUi(self)
        
        self.move(par.geometry().width()//2-self.geometry().width()//2,
                par.geometry().height()//2-self.geometry().height()//2)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timeFunc)
        self.timer.start(20)



    def timeFunc(self):
        # 定时器，目的是适配窗口并刷新内容
        self.move(self.par.geometry().width()//2-self.geometry().width()//2,
                  self.par.geometry().height()//2-self.geometry().height()//2)
        if self.redraw:
            if len(self.log) == 0:
                self.ui.logText.clear()
                self.__counter = 0
            else:
                for i in range(self.__counter, len(self.log)):
                    self.ui.logText.appendPlainText(self.log[i] + '\n')
                self.__counter = len(self.log)
            self.redraw = False

    def clearText(self):
        self.log.clear()
        self.__counter = 0
        self.ui.logText.clear()
    


