import os
from retinaface import Retinaface


def encode_facename(DeviceName):
    '''
    在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
    '''
    os.chdir(os.path.dirname(__file__))
    retinaface = Retinaface(1)

    list_dir = os.listdir("face_dataset")
    image_paths = []
    names = []
    for name in list_dir:
        image_paths.append("face_dataset/" + name)
        names.append(name.split("_")[0])
    #
    retinaface.encode_face_dataset(image_paths, names, DeviceName)


if __name__ == '__main__':
    encode_facename("NJXQLYFZYXGS-001")
