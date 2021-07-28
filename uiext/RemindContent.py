#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QHBoxLayout,\
    QListWidgetItem, QPlainTextEdit
import sqlite3

class RemindContent(QWidget):

    def __init__(self, *args, **kwargs):
        super(RemindContent, self).__init__()

        self.resize(800, 600)
        #左右布局(左边一个QListWidget + 右边QStackedWidget)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)
        # 右侧层叠窗口
        self.stackedWidget = QStackedWidget(self)
        self.resultView = QPlainTextEdit(self)
        self.resultView.setReadOnly(True)
        self.stackedWidget.addWidget(self.resultView)
        layout.addWidget(self.stackedWidget)

        self.id = kwargs.get('id')
        self.page_id = kwargs.get('pageid')

        self.initUi()

    def initUi(self):
        # 初始化界面
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)
        # 初始化信号
        self.listWidget.itemClicked.connect(self.onItemClicked)
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        with sqlite3.connect('db/risk.db') as conn:
            cursor = conn.cursor()
            results = cursor.execute("SELECT rc.id,rc.title,rc.content from page_remindtype rp,remindtype_content rc\
                        where rp.page_id='{}' and rp.type_id = rc.type_id order by rc.id ".format(self.page_id))
            rows = results.fetchall()
            # 初始化模拟数据
            for row in rows:
                id = str(row[0])
                text =  row[1]
                item = QListWidgetItem(QIcon('Data/0%d.ico' % randint(1, 8)), str(text), self.listWidget)
                item.setData(Qt.DisplayRole,text)
                item.setData(Qt.UserRole,id)
                 # 设置item的默认宽高(这里只有高度比较有用)
                item.setSizeHint(QSize(16777215, 60))
                # 文字居中
                item.setTextAlignment(Qt.AlignCenter)
                if self.id == id:
                    item.setSelected(True)
                    self.onItemClicked(item)  

    def onItemClicked(self, item):
        title = item.text()
        with sqlite3.connect('db/risk.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT rc.title,rc.content from remindtype_content rc\
                        where rc.title = ? ",(title,))
            row = cursor.fetchone()

            self.resultView.clear()
            self.resultView.appendHtml(f"{row[1]}")

            
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    #app.setStyleSheet(Stylesheet)
    w = RemindContent()
    w.show()
    sys.exit(app.exec_())
