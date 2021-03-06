package main

import (
	"encoding/binary"
	"net"
	"fmt"
)

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:3563")
	if err != nil {
		panic(err)
	}

	// Hello 消息（JSON 格式）
	// 对应游戏服务器 Hello 消息结构体
	data := []byte(`{
		"PLAYER_POSITION": {
			"pos_x": 300.13233,
			"pos_y": 200.13233
		}
	}`)

	// len + data
	m := make([]byte, 2+len(data))

	// 默认使用大端序
	binary.BigEndian.PutUint16(m, uint16(len(data)))

	copy(m[2:], data)

	fmt.Print(m)

	// 发送消息
	conn.Write(m)
}
