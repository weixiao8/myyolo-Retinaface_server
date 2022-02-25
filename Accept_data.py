############################
# 向管理平台推流：
# 将基于yolo4的待检测目标通过jetson nano的盒子推流到目标web上
# data数据中的deviceNo是需要在web平台上先注册的，非注册设备名称无法推流
# base64转码必须是jpg文件，否则无法在web平台上转码显示
########################
import base64
import json
import os
import time
from io import BytesIO

import requests
from PIL import Image


def AcceptFaceData(DeviceName):
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K) tuhuAndroid 5.24.6',
               'content-type': 'application/json',
               "secretKey": "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"
               }

    url = "http://njdt.njtjy.org.cn:10032/api/aiDevice/findFaceByDeviceNo" + "?aiDeviceNo=" + DeviceName
    data = {}  # Post请求发送的数据，字典格式
    # data需要转化成json才能post
    res = requests.get(url=url, data=json.dumps(data), headers=headers)  # 这里使用post方法，参数和get方法一样
    return res.json()
