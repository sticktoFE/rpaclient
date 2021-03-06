#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from random import choice, randint

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont, QIcon
from PyQt5.QtWidgets import QLabel, QMenu, QApplication

Style = """
QMenu {
    /* 半透明效果 */
    background-color: rgba(255, 255, 255, 230);
    border: none;
    border-radius: 4px;
}

QMenu::item {
    border-radius: 4px;
    /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
    padding: 8px 48px 8px 36px; /* 36px是文字距离左侧距离*/
    background-color: transparent;
}

/* 鼠标悬停和按下效果 */
QMenu::item:selected {
    border-radius: 0px;
    /* 半透明效果 */
    background-color: rgba(232, 232, 232, 232);
}

/* 禁用效果 */
QMenu::item:disabled {
    background-color: transparent;
}

/* 图标距离左侧距离 */
QMenu::icon {
    left: 15px;
}

/* 分割线效果 */
QMenu::separator {
    height: 1px;
    background-color: rgb(232, 236, 243);
}
"""


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


def about_qt():
    # 关于Qt
    QApplication.instance().aboutQt()



class RightMenu(QLabel):

    def __init__(self, *args, **kwargs):
        super(RightMenu, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        self.setAlignment(Qt.AlignCenter)
        self.setText('右键弹出菜单')
        self.context_menu = QMenu(self)
        self.init_menu()

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
        menu.addAction(get_icon(), '启动（全窗口监控）')
        menu.addAction(get_icon(), '启动（划区监控）')
        self.context_menu.addMenu(menu)
        self.context_menu.addSeparator()
        self.context_menu.addAction(get_icon(), '关闭', about_qt)
        self.context_menu.addSeparator()
        action = self.context_menu.addAction('选项', self.managerConfig)
        #action.setEnabled(0)
    def managerConfig(self):
        from ManagerConfig import ManagerConfig
        self.mc = ManagerConfig()
        self.mc.show()

if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    w = RightMenu()
    w.show()
    sys.exit(app.exec_())
