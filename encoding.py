import os

from Accept_data import AcceptFaceData
from retinaface import Retinaface


def encode_facename(DeviceName):
    '''
    在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
    '''
    os.chdir(os.path.dirname(__file__))
    retinaface = Retinaface(1)
    data = AcceptFaceData(DeviceName)
    datas  = data["data"]
    datas = datas["uploadFileList"]
    image_paths = []
    names = []
    for data in datas:
        image_paths.append(data["url"])
        names.append(data["name"])
    print(image_paths)
    print(names)
    retinaface.encode_face_dataset(image_paths, names, DeviceName)


if __name__ == '__main__':
    encode_facename("NJXQLYFZYXGS-001")
