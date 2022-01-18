#!/usr/bin/python
#coding=utf8

import socket
import struct
import time
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client.connect(("127.0.0.1", 3563))

while True:

    msg_data = b'''{"PLAYER_POSITION": {"pos_x": 300.13233, "pos_y": 200.13233}}'''

    # 计算len+data长度,len占2个字节,可设置
    msg_len = len(msg_data)

    # 将数据长度转换为大端序
    big_endian_head = struct.pack(">H", msg_len)
    # 构造数据
    fin_data = bytes(big_endian_head) + bytes(msg_data)

    print("SND MSG LEN: " + str(len(fin_data)))
    print("SND MSG: " + msg_data)  

    # 发送数据
    client.send(fin_data)

    # 接收数据
    info = client.recv(1024)
    # 解析数据长度
    rcv_msg_len = struct.unpack(">H",info[:2])[0]
    rsv_msg = str(info[2:rcv_msg_len+2])
    print("RCV MSG LEN: " + str(rcv_msg_len))
    print("RCV MSG: " + rsv_msg)


    position = json.loads(rsv_msg)
    pos_x = position["PLAYER_POSITION"]["Pos_x"]
    pos_y = position["PLAYER_POSITION"]["Pos_y"]

    # with open("client_location", "a") as f:
    #     f.write("player_position: {} {}\n".format(str(pos_x), str(pos_y)))

    time.sleep(1)

