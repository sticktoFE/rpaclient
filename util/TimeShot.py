from PyQt5.QtCore import pyqtSignal,QThread
import time,re
from util.DirectShot import shotScreen
from util.PictureOCR import upload_to_picbed
import sqlite3
#from server.server import OCRServer
# 装饰器，用于测量阻塞计时
def test_time(func1):
    def train(self):
        start_time = time.time()
        res = func1(self)
        end_time = time.time()
        print(end_time - start_time)
        # logger.info(f'the ocr parse time is {end_time-start_time} s')
        return res
    return train
class OCRServerThread(QThread):
    """
    启动服务线程
    """
    def __init__(self, *args, **kwargs):
        super(OCRServerThread, self).__init__()
        #self.server = OCRServer()
    def stop(self):
        self.server.stop_server()
    @test_time
    def run(self):
        print("进程开始")   
        self.server.startup()



class TimeShot(QThread):
    """
    对图片进行ocr识别，，功能服务，可单独放一个文件
    """
    signal = pyqtSignal(tuple)
    def __init__(self, *args, **kwargs):
        super(TimeShot, self).__init__()
        self.runCon = True
        self.main_win = kwargs.get('main_win')
        self.box = kwargs.get('box')
        #连接数据库
        #self.conn = None
        #self.signal.connect(self.refresh)
    def stop(self):
        self.runCon = False
        self.wait() 
        
    @test_time
    def run(self):
        print("进程开始")
        kk = 0
        with sqlite3.connect('db/risk.db') as conn:
            while self.runCon:
                kk = kk+1
                #print("在TimeShot run"+str(kk))
                time.sleep(7)  # 制造阻塞
                originalPixmap = shotScreen(self.box)
                out_info = upload_to_picbed(originalPixmap)
                if not out_info:
                    continue
                #-------------：：主题搜索判断点：：
                reg_chinese = u"([\u4e00-\u9fff]+)"
                pattern =  re.compile(reg_chinese)
                pic_text_list = []
                for info_list in out_info:
                    one_line_list_chinese = pattern.findall(info_list[1])
                    if one_line_list_chinese:
                        one_line = "；".join(one_line_list_chinese)
                        pic_text_list.append(one_line)
                        
                    else:
                        continue
                searchResult = "。".join(pic_text_list)
                #self.signal.emit(("0001","<p>"+searchResult+"</p>"))
                #根据页面指纹查询匹配的相应内容
                cursor = conn.cursor()
                rows = cursor.execute("SELECT page_id,key_content  from page_fingerprint").fetchall()
                # 识别匹配内容最多的就是要的page_id
                page_id = None
                m=0
                n=0
                for row in rows:
                    key_content = row[1].split("；")
                    n = 0
                    for key in key_content:
                        if key in searchResult:
                            n = n + 1
                    if n == len(key_content) and n>m:
                        m = n
                        page_id = row[0]
                
                if not page_id:
                    self.signal.emit(("Hide",))
                    continue
                results = cursor.execute("SELECT rc.id,rc.title,rc.content from page_remindtype rp,remindtype_content rc\
                    where rp.page_id='{}' and rp.type_id = rc.type_id order by rc.id".format(page_id))
                rows = results.fetchall()
                print('匹配上')
                return_str = [(str(row[0]),str(row[1])) for row in rows]
                self.signal.emit((page_id,return_str))
                cursor.close()

    