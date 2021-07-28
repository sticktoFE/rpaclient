from PyQt5.QtWidgets import QApplication

 #对当前激活的窗口进行截图          
def shotScreen(box):
    # Garbage collect any existing image first.
    originalPixmap = None       
    screen= QApplication.primaryScreen()#PyQt5
    originalPixmap = screen.grabWindow(QApplication.desktop().winId(),*box)#PyQt5
    return originalPixmap
    