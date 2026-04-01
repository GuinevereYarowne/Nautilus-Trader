# Nautilus 行情可视化看板
## 1. 架构设计
- 后端：Go原生标准库，提供行情数据/状态接口
- 前端：原生HTML+JS+Lightweight Charts，展示K线+成交量
- 数据：模拟Nautilus Trader行情数据，接口适配层简单直接

## 2. 运行指南
### 本地运行
1. 安装Go环境
2. 执行：go run main.go
3. 浏览器打开：http://localhost:8080

### Docker运行
1. 构建：docker build -t nautilus-dashboard .
2. 运行：docker run -p 8080:8080 nautilus-dashboard

## 3. 开源贡献总结
### Issue链接
https://github.com/nautechsystems/nautilus_trader/issues/XXXX

### 解决思路
问题：文档中BarData拼写错误为Bardata
修复：将文档中的Bardata修正为BarData，提升新手阅读体验w