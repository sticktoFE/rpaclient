import time
import requests
from configparser import ConfigParser
import logging
from PyQt5.QtCore import QByteArray,QBuffer,QIODevice
from PyQt5.QtGui import QPixmap

def get_shot_bytes(qPixmap):
    shot_bytes = QByteArray()
    buffer = QBuffer(shot_bytes)
    buffer.open(QIODevice.WriteOnly)
    shot_img = qPixmap.toImage()
    shot_img.save(buffer, 'png')
    return shot_bytes.data()

def upload_to_picbed(qPixmap):
        shot_bytes = get_shot_bytes(qPixmap)
        filename = "shot" + str(time.time()).split('.')[0] + '.jpg'
        files = {
            "file": (filename, shot_bytes, "image/jpeg")
        }
        cfg = ConfigParser()
        cfg.read('config.ini')
        headers = {
            "Cookie": cfg.get("picbed", 'cookie')
        }
        try:
            res = requests.post(cfg.get("picbed", 'api'), data={'compress': 960},files=files, headers=headers)
            status_code = res.json()['code']
            if status_code == 200:
                out_info = res.json()['data']['raw_out']
                return out_info
            else:
                logging.information('服务非正常返回',"not 200, code: {}".format(res.status_code))
        except Exception as e:
            print(e.args)