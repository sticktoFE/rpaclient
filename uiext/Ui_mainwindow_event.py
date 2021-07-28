from random import choice, randint
import string
from win32clipboard import *
from PyQt5.QtGui import QFont, QIcon,QKeySequence, QPainter,QPixmap,QCursor
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,QMenu\
    ,QSystemTrayIcon,QShortcut,QFileDialog,QGraphicsDropShadowEffect,QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt,QEvent,QSize
import sqlite3,time
from util.DrawShot import ScreenLabel
from util.DirectShot import shotScreen
from util.DrawShot import ScreenLabel
from util.TimeShot import TimeShot
from functools import partial
from ui.Ui_mainwindow import Ui_MainWindow

from .Ui_dialog_afterDraw_event import ShotDialog
from .RemindContent import RemindContent
from .ManagerConfig import ManagerConfig
from os import path

def get_icon():
    # 测试模拟图标
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.transparent)
    painter = QPainter()
    painter.begin(pixmap)
    painter.setFont(QFont('Webdings', 11))
    painter.setPen(Qt.GlobalColor(randint(4, 18)))
    painter.drawText(0, 0, 16, 16, Qt.AlignCenter,choice(string.ascii_letters))
    painter.end()
    return QIcon(pixmap)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,width,height):
        super().__init__()
        self.width = width
        self.height = height
        self.adjustSize()
        self.setupUi(self)
        self.screen = QApplication.primaryScreen()
        self.move(0, 0)
        # 这一行就是来设置窗口始终在顶端的。
        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint)#保持界面在最上层且无边框（去掉窗口标题） 
        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        #设置背景图片
        pare_pare_dir = path.dirname(path.dirname(path.abspath(__file__)))
        picfile = path.join(pare_pare_dir,"icon","newai08.png")
        self.label.setPixmap(QPixmap(picfile))
        picfile = path.join(pare_pare_dir,"icon","newai09.png")
        self.label_2.setPixmap(QPixmap(picfile))
    
        # 托盘行为
        self.action_quit = QAction("退出", self, triggered=self.close)
        self.action_show = QAction("主窗口", self, triggered=self.show)
        self.menu_tray = QMenu(self)
        self.menu_tray.addAction(self.action_quit)
        # 增加分割线
        self.menu_tray.addSeparator()
        self.menu_tray.addAction(self.action_show)
        # 设置最小化托盘
        self.tray = QSystemTrayIcon(QIcon('./icon/ai.png'), self)  # 创建系统托盘对象
        #self.tray.activated.connect(self.freeShot)  # 设置托盘点击事件处理函数
        self.tray.setContextMenu(self.menu_tray)
        # 快捷键
        QShortcut(QKeySequence("F1"), self, self.freeShot)
        
        ##右键菜单设置
        self.context_menu = QMenu(self)
        self.init_menu()

        #self.label_text.setStyleSheet("color:blue")
        #菜单链接到选项配置的事件
        # self.option = Option()
        # self.option_request.triggered.connect(self.option.exec_)#也可以用show
        #self.start.triggered.connect(self.startScreenshot)
      
        #打开程序就截屏一次
        self.resize(300, 200)
        self.move(30,0)

        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
        self.label_2.hide()
    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())
    def init_menu(self):
        # 背景透明
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self.context_menu.setWindowFlags(
            self.context_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        # 二级菜单
        menu = QMenu('启动', self.context_menu)
        # 背景透明
        menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        menu.setWindowFlags(menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        menu.addAction(get_icon(), '启动（全窗口监控）',self.startScreenshot)
        menu.addAction(get_icon(), '启动（划区监控）',self.startHandScreenshot)
        self.context_menu.addMenu(menu)
        self.context_menu.addSeparator()
        self.context_menu.addAction(get_icon(), '关闭', self.stopScreenshot)
        self.context_menu.addSeparator()
        action = self.context_menu.addAction('选项', self.managerConfig)
        #action.setEnabled(0)
    def managerConfig(self):
        self.mc = ManagerConfig()
        self.mc.show()

    def sizeHint(self):
        return QSize(600, 400)

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

    ##手工画范围截图
    def freeShot(self,width,height):
        """开始截图"""
        self.hide()
        self.label = ScreenLabel(width,height)
        self.label.showFullScreen()
        self.label.signal.connect(self.callback)
    def callback(self, pixmap):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        #截完图做啥操作
        dialog = ShotDialog(pixmap[0])
        dialog.exec_()
        if not self.isMinimized():
            self.show()  # 截图完成显示窗口

    #对当前激活的窗口进行截图            
    def shootScreen(self):
        if self.delaySpinBox.value() != 0:
             QApplication.beep()
        self.originalPixmap = shotScreen()
        #self.updateScreenshotLabel()
        if self.hideThisWindowCheckBox.isChecked():
            self.show()
    #手工截当前屏幕
    def newScreenshot(self):
        if self.hideThisWindowCheckBox.isChecked():
            self.hide()
        self.pushButton_shotCurrentWin.setDisabled(True)
        Qt.QTimer.singleShot(self.delaySpinBox.value() * 1000,self.shootScreen)
        self.pushButton_shotCurrentWin.setDisabled(False)
    #手工截当前屏幕内容保存          
    def saveScreenshot(self):
        format = 'png'
        initialPath = Qt.QDir.currentPath() + "/untitled." + format
        fileName,filetype = QFileDialog.getSaveFileName(self, "Save As",
                initialPath,
                "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
        if fileName:
            self.originalPixmap.save(fileName, format)
            print("file saved as  %s" % fileName)

    def closeEvent(self, event):
        # self.option.close()
        # self.remindtype.close()
        # self.remindtype_content.close()
        
        # self.page_fingerprint.close()
        # self.page_remindtype.close()
        if hasattr(self,"mc"):
            self.mc.hide()#隐藏配置菜单
        if hasattr(self,"rcwindow"):
            self.rcwindow.hide() #隐藏详情页
        with sqlite3.connect('db/risk.db') as conn:
            cursor = conn.cursor()
            cursor.execute("update log_remind_detect set status ='1',time='{}' where status ='0'"\
                .format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            conn.commit()
            cursor.close()
        #self.server.stop()
        event.accept()
            

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized():
            self.tray.showMessage("通知", "已最小化到托盘，点击开始截图")
            self.tray.show()
            self.hide()
    #启动截屏
    def startScreenshot(self):
        self.PO = TimeShot(main_win=self,box=(0,0,self.width,self.height))
        self.PO.start()
        self.PO.signal.connect(self.refresh)
    #划区启动截屏
    def startHandScreenshot(self):
        """开始截图"""
        self.hide()
        self.label = ScreenLabel(self.width,self.height)
        self.label.showFullScreen()
        #self.label.signal.connect(self.callback)
        self.label.signal.connect(self.afterDraw)
        
    def afterDraw(self, box):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        if not self.isMinimized():
            self.show()  # 截图完成显示窗口
        if box[0]=='esc':
            return
        self.PO = TimeShot(main_win=self,box=box[1])
        self.PO.start()
        self.PO.signal.connect(self.refresh)
    #停止截屏
    def stopScreenshot(self):  
        self.PO.stop()
        #self.label_text.setAutoFillBackground(False)

    def refresh(self, result):
        if result[0] =="Hide":
            self.label_2.hide()
        else:
            self.label_2.show()
            self.label_2.disconnect()
            self.label_2.setStyleSheet("QLabel { background-color : #99FFFF; color :#CCCCFF;font-size:13px; }")
            self.label_2.setAttribute(Qt.WA_TranslucentBackground, True)#背景透明
            self.label_2.addList(result[1])
            #self.label_2.setText(result[1])
            self.label_2.adjustSize()
            self.label_2.linkActivated.connect(partial(self.anchorClicked,result[0]))
            #print("到底几次=================="+result[1])
   
    def anchorClicked(self,page_id,link):
        self.rcwindow = RemindContent(pageid=page_id,id=link)
        self.rcwindow.show()
        
# if __name__ == "__main__":
#     app = QApplication(argv)
#     width = QApplication.desktop().screenGeometry().width()
#     height = QApplication.desktop().screenGeometry().height()
#     window = Main()
#     window.show() 
#     exit(app.exec_())
