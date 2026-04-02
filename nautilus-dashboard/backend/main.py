# backend/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
import random

app = FastAPI()

# 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_klines(count: int = 200, start_price: float = 100.0):
    """生成连续的模拟K线数据。

    - count: 数据点数量（默认200）
    - start_price: 起始价格
    返回格式与前端期望一致：list of {time, open, high, low, close, volume}
    时间以毫秒 epoch 表示，每个K线间隔为1天。
    """
    random.seed(42)
    klines = []
    # 从过去 count 天开始
    now = datetime.utcnow()
    start_day = now - timedelta(days=count)
    price = float(start_price)

    for i in range(count):
        ts = start_day + timedelta(days=i)
        # 随机波动：以当前价格为基础产生open/close
        open_p = price
        # 收盘在 open 的 +/- 2% 范围内
        change = random.uniform(-0.02, 0.02)
        close_p = round(open_p * (1 + change), 2)
        high_p = round(max(open_p, close_p) * (1 + random.uniform(0, 0.01)), 2)
        low_p = round(min(open_p, close_p) * (1 - random.uniform(0, 0.01)), 2)
        volume = int(random.uniform(500, 5000))

        klines.append(
            {
                "time": int(ts.replace(tzinfo=None).timestamp() * 1000),
                "open": round(open_p, 2),
                "high": high_p,
                "low": low_p,
                "close": close_p,
                "volume": volume,
            }
        )

        # 为下一根K线更新基准价，使用收盘价略微移动
        price = close_p * (1 + random.uniform(-0.005, 0.005))

    return klines


# 启动时生成模拟数据（可调整数量）
mock_klines = generate_klines(count=300, start_price=100.0)

@app.get("/api/klines")
async def get_klines(symbol: str = "BTCUSD", limit: int = 100):
    """获取K线数据"""
    return {
        "symbol": symbol,
        "data": mock_klines[-limit:],
        "status": "OK"
    }

@app.get("/api/status")
async def get_status():
    """获取运行状态"""
    return {
        "connected": True,
        "venue": "BINANCE",
        "symbols": ["BTCUSD", "ETHUSD"],
        "uptime": "2h 30m"
    }

@app.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    """实时成交数据WebSocket"""
    await websocket.accept()
    try:
        while True:
            # 模拟实时数据推送
            # 基于最近一根K线的收盘价生成随机trade
            last_close = mock_klines[-1]["close"] if mock_klines else 100.0
            # 模拟价格微幅波动
            price = round(last_close * (1 + random.uniform(-0.002, 0.002)), 2)
            quantity = round(random.uniform(0.1, 2.0), 4)
            side = random.choice(["BUY", "SELL"])

            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "price": price,
                "quantity": quantity,
                "side": side,
            }
            await websocket.send_text(json.dumps(data))
            # 频率：每1秒推送一次
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)