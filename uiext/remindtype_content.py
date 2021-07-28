#导入包
from sys import argv,exit
from sqlite3 import connect
from functools import partial
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame,QApplication,QDialog, QDialogButtonBox, QLabel,
        QMessageBox,QVBoxLayout, QLineEdit,QTableWidgetItem,QTableWidget,
        QAbstractItemView,QHeaderView,QComboBox)

#建立界面类
class RemindTypeContent(QLabel):
    def __init__(self,parent = None):
        super(RemindTypeContent,self).__init__(parent)

        #设置界面大小、名称、背景
        self.resize(1000,800)
        self.setWindowTitle('Database')
        #self.setStyleSheet("background-image:url(icon/tubiao_meitu.jpg)")
        #窗体属性
        self.setWindowFlags(Qt.Widget)
        #连接数据库
        db = connect("db/risk.db")
        #获取游标、数据
        cur = db.cursor()
        # #数据列名
        self.col_lst = None
        #插入表格
        self.MyTable = QTableWidget()
        font = QFont('微软雅黑',10)
        #查询框
        self.qle = QLineEdit()
        self.inq_data(cur,db)
        
        #设置字体、表头
        self.MyTable.horizontalHeader().setFont(font)
        self.col_lst = [tup[0] for tup in cur.description]
        self.MyTable.setHorizontalHeaderLabels(self.col_lst)
        #self.MyTable.setHorizontalHeaderLabels(['姓名', '性别', '体重(kg)'])
        #设置竖直方向表头不可见
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.NoFrame)

        self.MyTable.setSelectionBehavior(QAbstractItemView.SelectRows)#設置表格的選取方式是行選取
        self.MyTable.setSelectionMode(QAbstractItemView.SingleSelection)#設置選取方式爲單個選取
        
        #设置表格颜色             
        self.MyTable.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.MyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.MyTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        
        buttonBox = QDialogButtonBox()
        #增删查改四个按钮
        inquireButton = buttonBox.addButton("查询",QDialogButtonBox.ActionRole)
        addButton = buttonBox.addButton("新增",QDialogButtonBox.ActionRole)
        okButton = buttonBox.addButton("保存",QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("删除",QDialogButtonBox.ActionRole)

        #设置按钮内字体样式
        addButton.setFont(font)
        okButton.setFont(font)
        deleteButton.setFont(font)
        inquireButton.setFont(font)

        #垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.qle)
        layout.addWidget(buttonBox)
        layout.addWidget(self.MyTable)
        self.setLayout(layout)
        addButton.clicked.connect(partial(self.add_data,cur,db))#插入实现
        okButton.clicked.connect(partial(self.up_data, cur, db,self.col_lst))#插入实现
        deleteButton.clicked.connect(partial(self.del_data,cur,db))#删除实现
        inquireButton.clicked.connect(partial(self.inq_data,cur,db))#查询实现
        self.MyTable.itemChanged.connect(partial(self.table_update,cur,db))
    #查询
    def inq_data(self,cur,db):
        remindType = cur.execute("select type_id,type_name from remindType").fetchall()
        txt = self.qle.text()
        #模糊查询
        sql = f"SELECT * FROM remindtype_content WHERE title LIKE '%{txt}%' or content LIKE '%{txt}%'"
        cur.execute(sql)
        data_x = cur.fetchall()
        row_4 = len(data_x)
        vol_1 = len(cur.description)
        self.MyTable.clearContents()
        self.MyTable.setColumnCount(vol_1)
        self.MyTable.setRowCount(row_4) 
        #查询到的更新带表格当中
        for i_x in range(row_4):
            for j_y in range(vol_1):
                temp_data_1 = data_x[i_x][j_y]  # 临时记录，不能直接插入表格
                if j_y == 1:
                     #设置下拉框
                    comBox = QComboBox()
                    for onerow in remindType:
                        comBox.addItem(onerow[1],onerow[0])
                    comBox.setCurrentText(temp_data_1)
                    comBox.setStyleSheet("QComboBox{margin:3px};")
                    comBox.currentIndexChanged.connect(partial(self.comboxSelect,cur,db,i_x,j_y,comBox)) #绑定combox select 事件
                    self.MyTable.setCellWidget(i_x, j_y, comBox)    
                else:
                    data_1 = QTableWidgetItem(str(temp_data_1))  # 转换后可插入表格
                    if j_y ==0 or j_y ==2:
                        # 設置物件的狀態爲只可被選擇（未設置可編輯）
                        data_1.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  
                    self.MyTable.setItem(i_x, j_y, data_1)
    
    #添加空表格 --默认第一个字段都是 自增长的id主键
    def add_data(self,cur,db):
        #获取行数
        row = self.MyTable.rowCount()
        if self.MyTable.item(row-1,0) and not self.MyTable.item(row-1,0).text():
            QMessageBox.about(self, 'Message', '请先保存再新增')
            return
        #在末尾插入一空行
        self.MyTable.insertRow(row)
        #逐渐id
        item_id = QTableWidgetItem("")
        item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 設置物件的狀態爲只可被選擇（未設置可編輯）
        self.MyTable.setItem(row, 0, item_id)
        #设置下拉框
        cur.execute("select type_id,type_name from remindType")
        results = cur.fetchall()
        comBox = QComboBox()
        #comBox.currentIndexChanged.connect(partial(self.comboxSelect,row)) #绑定combox select 事件
        for onerow in results:
            comBox.addItem(onerow[1],onerow[0])
        comBox.setStyleSheet("QComboBox{margin:3px};")
        self.MyTable.setCellWidget(row, 1, comBox)
        #码值列不可编辑
        item_id = QTableWidgetItem("")
        item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 設置物件的狀態爲只可被選擇（未設置可編輯）
        self.MyTable.setItem(row, 2, item_id)
    #保存数据 
    def up_data(self,cur,db,col_lst):
        row_1 = self.MyTable.rowCount()
        if self.MyTable.item(row_1-1,0) and self.MyTable.item(row_1-1,0).text():
            QMessageBox.about(self, 'Message', '请先新增再保存')
            return
        value_lst = []
        for i in range(len(col_lst)):
            if i==2:
                continue
            if i==1:
                oneitem = self.MyTable.cellWidget(row_1-1,i)
                if not oneitem:
                    value_lst.append(None)
                else:
                    value_lst.append(oneitem.currentText())
                    value_lst.append(oneitem.currentData())
            else:
                oneitem = self.MyTable.item(row_1-1,i)
                if not oneitem:
                    value_lst.append(None)
                else:
                    value_lst.append(oneitem.text())
        #插入语句 默认第一个字段都是 自增长的id主键 所以下面从第二个字段开始组装语句
        cols = ','.join(col_lst[1:])
        values = ','.join(f"'{value}'" for value in value_lst[1:])
        cur.execute(f"INSERT INTO remindtype_content({cols}) VALUES ({values})")
        db.commit()
        self.inq_data(cur,db)
    def comboxSelect(self,cur,db,i_x,j_y,comBox):
        id = self.MyTable.item(i_x,0).text()
        row_select = self.MyTable.selectedItems()
        if len(row_select) == 0 or not id:
            return
        # 以下可以加入保存數據到數據的操作
        #更新语句 #modify
        upsets = f"{self.col_lst[j_y]}='{comBox.currentText()}',{self.col_lst[j_y+1]}='{comBox.currentData()}'"
        wheres = f"{self.col_lst[0]}={id}" #其实默认都是id
        cur.execute(f"update remindtype_content set {upsets} where {wheres}")
        db.commit()
        self.inq_data(cur,db)
    #update
    def table_update(self,cur,db,item):
        id = self.MyTable.item(item.row(),0).text()
        row_select = self.MyTable.selectedItems()
        if len(row_select) == 0 or not id:
            return
        # 以下可以加入保存數據到數據的操作
        #更新语句
        upsets = f"{self.col_lst[item.column()]}='{item.text()}'"
        wheres = f"{self.col_lst[0]}={id}" #其实默认都是id
        cur.execute(f"update remindtype_content set {upsets} where {wheres}")
        db.commit()
        #self.inq_data(cur,db)
    #删除
    def del_data(self,cur,db):
        row_select = self.MyTable.selectedItems()
        if len(row_select) == 0:
            return
        #是否删除的对话框
        reply = QMessageBox.question(self, 'Message', 'Are you sure to delete it ?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply ==  QMessageBox.Yes:
            #当前行
            row_2 = self.MyTable.currentRow()
            del_d = self.MyTable.item(row_2, 0).text()
            #在数据库删除数据
            cur.execute(f"DELETE FROM remindtype_content WHERE id = {del_d}")
            db.commit()
            #删除表格
            self.MyTable.removeRow(row_2)
if __name__ == '__main__':
    #显示
    app = QApplication(argv)
    c = RemindTypeContent()
    c.show()

    exit(app.exec_())
