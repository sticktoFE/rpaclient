#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QHBoxLayout,\
    QListWidgetItem
from .Ui_option_event import Option
from .remindtype import RemindType
from .remindtype_content import RemindTypeContent
from .page_fingerprint import PageFingerprint
from .page_remindtype import PageRemindtype

class ManagerConfig(QWidget):

    def __init__(self, *args, **kwargs):
        super(ManagerConfig, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        #左右布局(左边一个QListWidget + 右边QStackedWidget)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)
        # 右侧层叠窗口
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)
        self.initUi()

    def initUi(self):
        # 初始化界面
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 这里就用一般的文本配合图标模式了(也可以直接用Icon模式,setViewMode)
        item = QListWidgetItem(QIcon('Data/0%d.ico' % randint(1, 8)), str('页面提醒'), self.listWidget)
        # 设置item的默认宽高(这里只有高度比较有用)
        item.setSizeHint(QSize(16777215, 60))
        # 文字居中
        item.setTextAlignment(Qt.AlignCenter)

        item = QListWidgetItem(QIcon('Data/0%d.ico' % randint(1, 8)), str('提醒内容'), self.listWidget)
        # 设置item的默认宽高(这里只有高度比较有用)
        item.setSizeHint(QSize(16777215, 60))
        # 文字居中
        item.setTextAlignment(Qt.AlignCenter)

        item = QListWidgetItem(QIcon('Data/0%d.ico' % randint(1, 8)), str('提醒类型'), self.listWidget)
        # 设置item的默认宽高(这里只有高度比较有用)
        item.setSizeHint(QSize(16777215, 60))
        # 文字居中
        item.setTextAlignment(Qt.AlignCenter)

        item = QListWidgetItem(QIcon('Data/0%d.ico' % randint(1, 8)), str('页面关键字'), self.listWidget)
        # 设置item的默认宽高(这里只有高度比较有用)
        item.setSizeHint(QSize(16777215, 60))
        # 文字居中
        item.setTextAlignment(Qt.AlignCenter)

        item = QListWidgetItem(QIcon('Data/0%d.ico' % randint(1, 8)), str('服务网络配置'), self.listWidget)
        # 设置item的默认宽高(这里只有高度比较有用)
        item.setSizeHint(QSize(16777215, 60))
        # 文字居中
        item.setTextAlignment(Qt.AlignCenter)

        self.PageRemindtype = PageRemindtype()
        self.stackedWidget.addWidget(self.PageRemindtype)

        self.RemindTypeContent = RemindTypeContent()
        self.stackedWidget.addWidget(self.RemindTypeContent)

        self.RemindType = RemindType()
        self.stackedWidget.addWidget(self.RemindType)

        self.PageFingerprint = PageFingerprint()
        self.stackedWidget.addWidget(self.PageFingerprint)

        self.Option = Option()
        self.stackedWidget.addWidget(self.Option)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    #app.setStyleSheet(Stylesheet)
    w = ManagerConfig()
    w.show()
    sys.exit(app.exec_())
