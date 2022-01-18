#!/usr/bin/python
#coding=utf8

from pyglet.window import key
from cocos import actions, layer, sprite, scene
from cocos.director import director
from cocos.actions import *
import socket
import struct
import json


# Player class

class Me(actions.Move):

    # step() is called every frame.
    # dt is the number of seconds elapsed since the last call.
    def step(self, dt):

        super(Me, self).step(dt) # Run step function on the parent class.


        # Set the object's velocity. 
        velocity_x = 200 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 200 * (keyboard[key.UP] - keyboard[key.DOWN])
        
        if self.target.position[0] > 960:
            self.target.velocity = (-100, velocity_y)
        elif self.target.position[0] < 0:
            self.target.velocity = (100, velocity_y)
        elif self.target.position[1] < 0:
            self.target.velocity = (velocity_x, 100)
        elif self.target.position[1] > 640:
            self.target.velocity = (velocity_x, -100)
        else:
            self.target.velocity = (velocity_x, velocity_y)
        

class Frame_Sync(actions.Move):
    def __init__(self, player_id, client):
        super(Frame_Sync, self).__init__()
        self.player_id = player_id
        self.client = client
    def step(self, dt):
        super(Frame_Sync, self).step(dt)
        print(self.target.position)
        msg_data = b'{"PLAYER_STATUS": {"id": %s, "pos_x": %s, "pos_y": %s}}' % (self.player_id, self.target.position[0], self.target.position[1])
        # 计算len+data长度,len占2个字节,可设置
        msg_len = len(msg_data)

        # 将数据长度转换为大端序
        big_endian_head = struct.pack(">H", msg_len)
        # 构造数据
        fin_data = bytes(big_endian_head) + bytes(msg_data)
        print("SND MSG LEN: " + str(len(fin_data)))
        print("SND MSG: " + msg_data)  
        # 发送数据
        self.client.send(fin_data)
        # 接收数据
        info = self.client.recv(1024)
        # 解析数据长度
        rcv_msg_len = struct.unpack(">H",info[:2])[0]
        rsv_msg = str(info[2:rcv_msg_len+2])
        print("RCV MSG LEN: " + str(rcv_msg_len))
        print("RCV MSG: " + rsv_msg)

        position = json.loads(rsv_msg)
        id = position["PLAYER_STATUS"]["Id"]
        pos_x = position["PLAYER_STATUS"]["Pos_x"]
        pos_y = position["PLAYER_STATUS"]["Pos_y"]
        if id == self.player_id:
            self.target.position = (pos_x, pos_y)


# Main class

def run_scene():
    global keyboard # Declare this as global so it can be accessed within class methods.

    # Initialize the window.
    director.init(width=960, height=640, autoscale=False, resizable=True)

    # Create a layer and add a sprite to it.
    player_layer = layer.Layer()
    bg = sprite.Sprite('images/bg1.jpeg')
    me = sprite.Sprite('images/ufo1.png')
    him = sprite.Sprite('images/ufo1.png')
    player_layer.add(bg)
    player_layer.add(me)
    player_layer.add(him)

    # Set initial position and velocity.
    bg.position = (480, 320)
    me.position = (400, 100)
    me.velocity = (0, 0)
    him.position = (400, 100)
    him.velocity = (0, 0)

    # Set the sprite's movement class.
    me.do(Me())
    player_id = 2
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client.connect(("127.0.0.1", 3563))
    me.do(Frame_Sync(player_id, client))
    player_id = 1
    him.do(Frame_Sync(player_id, client))

    # me.do(RotateBy(180, duration=3))

    # Create a scene and set its initial layer.
    main_scene = scene.Scene(player_layer)

    # Attach a KeyStateHandler to the keyboard object.
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    # Play the scene in the window.
    director.run(main_scene)


if __name__ == '__main__':
    run_scene()








# 背景音乐下载
# https://www.sucaibar.com/yinxiao/chunyinyue.html


# 安装模块
# pip install pyglet==1.4.10
# pip install cocos2d


# cocos2d python samples
# https://github.com/los-cocos/cocos/tree/master/samples
# tutorials
# https://github.com/liamrahav/cocos2d-python-tutorials/tree/master/basics