# Nautilus 行情可视化看板
## 1. 架构设计
- 后端：python原生标准库，提供行情数据/状态接口
- 前端：原生HTML+JS+Lightweight Charts，展示K线+成交量
- 数据：模拟Nautilus Trader行情数据，接口适配层简单直接

## 2. 运行指南
### 本地运行
1. 安装python环境
2. 在 nautilus-dashboard/backend 目录启动后端，python main.py
3. 在nautilus-dashboard/frontend目录启动前端，npm start
4. 也可以在nautilus-dashboard目录下docker一键启动
docker-compose up --build
5. 浏览器打开：http://localhost:3000

## 3. 开源贡献总结
### Issue链接
https://github.com/nautechsystems/nautilus_trader/issues/3778

## Description问题描述
修复了Binance期货尾随止损订单的两个bug

## Issues Fixed
Fixes #3778

## Changes Made
1. **参数名修复**：将 `activationPrice` 改为 `activatePrice`
   - 符合Binance官方API文档
   - 确保激活价格被正确传递

2. **精度恢复**：移除callback_rate的四舍五入
   - 25基点 (25 bps) 现在正确转换为 0.25%
   - 之前错误地四舍五入为 0.2%

## Testing
- 通过了现有单元测试
- 新增测试用例验证参数正确性
- 在testnet环境验证有效

## Related
- #3778 (parent issue)
