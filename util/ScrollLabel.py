from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import Qt,QTimer

class ScrollLabel(QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        self.list = []
        
    def addList(self,rowlist):
        self.fontWidth = QFontMetrics(super().font())
        self.list = list(map(lambda row:(row[0],self.fontWidth.elidedText(row[1], Qt.ElideRight, 100)),rowlist)) #最大宽度100像素
        self.nn=0  
         #跑马灯
        self.pTimer = QTimer()
        self.pTimer.timeout.connect(self.display)
        #定时200毫秒
        self.pTimer.start(1000);
    def enterEvent(self,event):
        self.pTimer.stop()
        event.accept()
        
    def leaveEvent(self,event):
        self.pTimer.start()
        event.accept()

    def display(self):
        if self.nn < len(self.list)-3:
            innerHtml = [f"<p><a href='{str(item[0])}'>"+str(item[1])+"</a></p>" for item in self.list[self.nn:self.nn+4]]
            self.setText("".join(innerHtml))
            self.nn = self.nn+1
        else:
            innerHtml = [f"<p><a href='{str(item[0])}'>"+str(item[1])+"</a></p>" for item in self.list[self.nn:]]
            self.setText("".join(innerHtml))
            self.nn = 0