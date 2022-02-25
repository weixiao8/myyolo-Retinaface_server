import base64
import os
from django.http import HttpResponse, JsonResponse
import json
import sys

sys.path.append("../")
from encoding import encode_facename

secretKey = "E93C5337F00C258C5244670822F81DE5E7566EE1594CBD525279DA82EC18617F"


def is_base64_code(s):
    '''Check s is Base64.b64encode'''
    if not isinstance(s, str) or not s:
        raise ValueError("params s not string or None")

    _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                    '2', '3', '4', '5', '6', '7', '8', '9', '+',
                    '/', '=']

    # Check base64 OR codeCheck % 4
    code_fail = [i for i in s if i not in _base64_code]
    if code_fail or len(s) % 4 != 0:
        return False
    return True


# 增加人脸
def add_face(request):
    if request.method == "POST":
        key = request.META.get("HTTP_SECRETKEY", b'')
        if key != secretKey:
            return JsonResponse({"state": "501", "msg": "秘钥错误，请检查秘钥！"})
        data = json.loads(request.body)
        name = data["facename"]
        if len(name) < 2 or len(name) > 4:
            return JsonResponse({"state": "500", "msg": "人脸姓名字数异常！"})
        jpg_base64 = data["jpg"][22:]
        if not is_base64_code(jpg_base64):
            return JsonResponse({"state": "500", "msg": "编码异常！请检查传参！"})
        imagedata = base64.b64decode(jpg_base64)
        filename = "../face_dataset/" + name + "_1.jpg"
        file = open(filename, "wb")
        file.write(imagedata)
        file.close()
        if file:
            return JsonResponse({"state": "200", "msg": "添加人脸成功！"})
        else:
            return JsonResponse({"state": "500", "msg": "添加人脸失败！"})


# python manage.py runserver 10.2.13.4:8000

# 删除人脸
def delete_face(request):
    if request.method == "DELETE":
        key = request.META.get("HTTP_SECRETKEY", B'')
        if key != secretKey:
            return JsonResponse({"state": "501", "msg": "秘钥错误，请检查秘钥！"})
        data = json.loads(request.body)
        name = data["facename"]
        if len(name) < 2 or len(name) > 4:
            return JsonResponse({"state": "500", "msg": "人脸姓名字数异常！"})
        filename = "../face_dataset/" + name + "_1.jpg"
        if os.path.exists(filename):
            os.remove(filename)
            return JsonResponse({"state": "200", "msg": "删除人脸成功！"})
        else:
            return JsonResponse({"state": "500", "msg": "未找到该人脸！"})


# 增删人脸之后需要将整个检测模块重启！

def encode_face(request):
    if request.method == "POST":
        key = request.META.get("HTTP_SECRETKEY", B'')
        if key != secretKey:
            return JsonResponse({"state": "501", "msg": "秘钥错误，请检查秘钥！"})
        #####################################################################
        # 编码会产生两个.npy文件
        # 第二次编码会强制清空所有npy文件以保证websocket逻辑正确
        # 如果断网等原因导致人脸库更新失败需要重新生成人脸文件
        #####################################################################
        data = json.loads(request.body)
        DeviceName = data["DeviceName"]
        encode_facename(DeviceName)
        return JsonResponse({"state": "200", "msg": "人脸编码成功！新的人脸识别库将在数分钟内更新完成！"})
