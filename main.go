// 新手版：Go行情数据接口
// 仅用原生标准库，无任何框架
package main

import (
	"encoding/json"
	"net/http"
	"time"
)

// 模拟K线数据（对应Nautilus的Bar数据）
type Kline struct {
	Time   int64   `json:"time"`   // 时间
	Open   float64 `json:"open"`   // 开盘价
	High   float64 `json:"high"`   // 最高价
	Low    float64 `json:"low"`    // 最低价
	Close  float64 `json:"close"`  // 收盘价
	Volume float64 `json:"volume"` // 成交量
}

// 系统状态数据
type SystemStatus struct {
	Running string `json:"running"` // 运行状态
	Venue   string `json:"venue"`   // 交易所状态
}

// 首页接口
func homeHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Nautilus 行情看板后端服务运行中！"))
}

// 返回K线数据接口
func klineHandler(w http.ResponseWriter, r *http.Request) {
	// 模拟10条K线数据（新手模拟数据，代替Nautilus真实数据）
	var klines []Kline
	now := time.Now().Unix()
	for i := 0; i < 10; i++ {
		klines = append(klines, Kline{
			Time:   now - int64(10-i)*60,
			Open:   50000 + float64(i)*100,
			High:   50000 + float64(i)*150,
			Low:    50000 + float64(i)*50,
			Close:  50000 + float64(i)*120,
			Volume: 1.5 + float64(i)*0.2,
		})
	}

	// 返回JSON数据
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(klines)
}

// 返回系统状态接口
func statusHandler(w http.ResponseWriter, r *http.Request) {
	status := SystemStatus{
		Running: "正常运行",
		Venue:   "已连接币安交易所",
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func main() {
	// 注册3个接口
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/api/kline", klineHandler)   // 行情K线接口
	http.HandleFunc("/api/status", statusHandler) // 系统状态接口

	// 启动服务，端口8080
	println("后端服务启动：http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}
