package msg

import (
	"github.com/name5566/leaf/network/json"
)

// 使用默认的 JSON 消息处理器（默认还提供了 protobuf 消息处理器）
var Processor = json.NewProcessor()

func init() {
	// 这里我们注册了一个 JSON 消息 PLAYER_STATUS
	Processor.Register(&PLAYER_STATUS{})
}

// 一个结构体定义了一个 JSON 消息的格式
// 消息名为 PLAYER_STATUS
type PLAYER_STATUS struct {
	Id   int
	Pos_x float32
	Pos_y float32
}
