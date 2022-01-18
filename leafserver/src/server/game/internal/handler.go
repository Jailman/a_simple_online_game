package internal

import (
	"github.com/name5566/leaf/log"
	// "github.com/name5566/leaf/gate"
	"reflect"
	"server/msg"
)

func init() {
	// 向当前模块（game 模块）注册 PLAYER_STATUS 消息的消息处理函数 handleplayerstatus
	handler(&msg.PLAYER_STATUS{}, handleplayerstatus)
}

func handler(m interface{}, h interface{}) {
	skeleton.RegisterChanRPC(reflect.TypeOf(m), h)
}

func handleplayerstatus(args []interface{}) {
	// 收到的 PLAYER_POSITION 消息
	m := args[0].(*msg.PLAYER_STATUS)
	// 消息的发送者
	// a := args[1].(gate.Agent)

	// 输出收到的消息的内容
	log.Debug("PLAYER_STATUS: %v,%v,%v", m.Id, m.Pos_x, m.Pos_y)

	// 给发送者回应一个 PLAYER_POSITION 消息
	// a.WriteMsg(&msg.PLAYER_POSITION{
	// 	Pos_x: m.Pos_x,
	// 	Pos_y: m.Pos_y,
	// })

	for a := range agents {
		a.WriteMsg(&msg.PLAYER_STATUS{
			Id:   m.Id,
			Pos_x: m.Pos_x,
			Pos_y: m.Pos_y,
		})
	}
}
