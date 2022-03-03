import os
import time

from Accept_data import AcceptFaceData
from retinaface import Retinaface
# coding: utf8
import requests


def clear_dir(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            time.sleep(0.1)
            os.remove(path_file)
        else:
            for f in os.listdir(path_file):
                path_file2 = os.path.join(path_file, f)
                if os.path.isfile(path_file2):
                    os.remove(path_file2)


def download_img(img_url, name):
    # os.chdir(os.path.dirname(__file__))
    api_token = "fklasjfljasdlkfjlasjflasjfljhasdljflsdjflkjsadljfljsda"
    header = {"Authorization": "Bearer " + api_token}  # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    r = requests.get(img_url, headers=header, stream=True)
    if r.status_code == 200:
        filename = r"face_dataset/" + name + r".jpg"
        open(filename, 'wb').write(r.content)  # 将内容写入图片
    del r


def encodelist(DeviceName):
    """
    在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
    """
    # os.chdir(os.path.dirname(__file__))
    retinaface = Retinaface(1)
    list_dir = os.listdir("face_dataset")
    image_paths = []
    names = []
    for name in list_dir:
        image_paths.append("face_dataset/" + name)
        names.append(name)
    retinaface.encode_face_dataset(image_paths, names, DeviceName)


def encode_facename(DeviceName):
    """
    在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
    """
    print(os.getcwd())
    os.chdir(os.path.dirname(__file__))
    print(os.getcwd())
    clear_dir("./face_dataset")
    data = AcceptFaceData(DeviceName)
    datas = data["data"]
    datas = datas["uploadFileList"]
    print(datas)
    if datas != None:
        for data in datas:
            download_img(data["url"], data["name"])
        encodelist(DeviceName)
        return "200"
    else:
        return "500"


if __name__ == '__main__':
    encode_facename("NJXQLYFZYXGS-001")
