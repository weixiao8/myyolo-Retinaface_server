import asyncio
import time

import websockets
import socket, os, struct


# 检测客户端权限，用户名密码通过才能退出循环
async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)


async def send_npy(filepath, websocket):
    fmt = '128si'
    send_buffer = 409600
    if os.path.exists(filepath):
        time.sleep(0.1)
        filename = os.path.split(filepath)[1]
        filesize = os.path.getsize(filepath)
        print("filename:" + filename + "\nfilesize:" + str(filesize))
        head = struct.pack(fmt, filename.encode(), filesize)
        print(r"\nhead size:" + str(head.__len__()) + "\n" + str(head))
        await websocket.send(head)
        restSize = filesize
        fd = open(filepath, 'rb')
        count = 0
        while restSize >= send_buffer:
            data = fd.read(send_buffer)
            await websocket.send(data)
            restSize = restSize - send_buffer
            print(str(count) + " ")
            count = count + 1
        data = fd.read(restSize)
        await websocket.send(data)
        fd.close()
        print("successfully sent")
        os.remove(filepath)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket):
    fmt = '128si'
    # 服务端接受客户端发送的设备名称
    deviceid = await websocket.recv()
    print(deviceid)
    ################################################################
    # 解析生成的设备所需的人脸编码数据和对应的人脸名称的.npy文件
    # 需要将文件名中设备名称提取出来，通过提取的设备名称将对应发送不同的设备
    # 设备名称必须第一无二
    # 生成.npy文件的接口不可以频繁调用
    ################################################################
    file = "./model_data_facenpy/"
    list_device = os.listdir(file)
    #################################################################
    # 判断是否生成了npy文件
    # 若没有生成发送404错误代码
    #################################################################
    if len(list_device) != 2:
        await  websocket.send(struct.pack(fmt, "404".encode(), 0))
        await  websocket.send(struct.pack(fmt, "404".encode(), 0))
    DeviceName = list_device[0].split("-")[1]
    deviceid = deviceid + ".npy"
    ################################################################
    # 判断给哪个设备发送npy
    # 非对应设备会接受到404的信号
    ################################################################
    if deviceid == DeviceName:
        send_buffer = 409600
        filepath = "./model_data_facenpy/"
        filepath += list_device[0]
        await send_npy(filepath, websocket)

        filepath = "./model_data_facenpy/"
        filepath += list_device[1]
        await send_npy(filepath, websocket)
    else:
        await  websocket.send(struct.pack(fmt, "404".encode(), 0))
        await  websocket.send(struct.pack(fmt, "404".encode(), 0))


# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)


# 把ip换成自己本地的ip
start_server = websockets.serve(main_logic, '0.0.0.0', 2022)
# 如果要给被回调的main_logic传递自定义参数，可使用以下形式
# 一、修改回调形式
# import functools
# start_server = websockets.serve(functools.partial(main_logic, other_param="test_value"), '10.10.6.91', 5678)
# 修改被回调函数定义，增加相应参数
# async def main_logic(websocket, path, other_param)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
