from smbus2 import SMBus
from bmp180_min import BMP180
import requests, time

TOKEN = "3aOkPW3pzGhHqSR0gPOofifBDM8kMRAVZneAmE8bYEUcxh1fLxsOX8ReMWXVOAsfFGvsyKpRziU54PIG56+1y46R9zm7G1Z7VQ/E3uMTR4fdel5+Xub+ZeJ9BfwiWa+Dcfc6Ois26bfIBy3zBk0TuQdB04t89/1O/w1cDnyilFU="
url = "https://api.line.me/v2/bot/message/broadcast"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

bus = SMBus(1)
bmp = BMP180(bus, address=0x77, oversample=3)
bmp.sea_level_pressure = 101325

while True:
    t = bmp.temperature
    p = bmp.pressure
    alt = bmp.altitude
    msg = f"🌡温度:{t:.2f}℃\n🧭気圧:{p:.0f}Pa\n⛰高度:{alt:.2f}m"

    body = {"messages": [{"type": "text", "text": msg}]}
    requests.post(url, headers=headers, json=body)
    print("送信:", msg)
    time.sleep(600)  # 10分ごと
