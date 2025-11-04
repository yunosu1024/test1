from smbus2 import SMBus
from bmp180_min import BMP180
import requests, time

TOKEN = "3aOkPW3pzGhHqSR0gPOofifBDM8kMRAVZneAmE8bYEUcxh1fLxsOX8ReMWXVOAsfFGvsyKpRziU54PIG56+1y46R9zm7G1Z7VQ/E3uMTR4fdel5+Xub+ZeJ9BfwiWa+Dcfc6Ois26bfIBy3zBk0TuQdB04t89/1O/w1cDnyilFU="

# Messaging APIのチャネルアクセストークン
url = "https://api.line.me/v2/bot/message/broadcast"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# === BMP180設定 ===
bus = SMBus(1)
bmp = BMP180(bus, address=0x77, oversample=3)
bmp.sea_level_pressure = 101325

# === メインループ ===
while True:
    t = bmp.temperature
    p = bmp.pressure
    alt = bmp.altitude

    # ---- 条件付きメッセージ生成 ----
    advice = ""

    # 温度に応じたコメント
    if t >= 30:
        advice += "🥵 暑さに注意！こまめに水分を取りましょう。\n"
    elif t <= 5:
        advice += "🥶 寒さに注意！防寒対策を忘れずに。\n"

    # 気圧に応じたコメント（低気圧は1010hPa ≒ 101000Pa以下）
    if p <= 100500:
        advice += "🌧 低気圧傾向です。体調や頭痛に注意しましょう。\n"
    elif p >= 102500:
        advice += "🌤 高気圧です。穏やかな天気が続きそうです。\n"

    # ---- 本文メッセージ ----
    msg = (
        f"🌡温度: {t:.2f} ℃\n"
        f"🧭気圧: {p:.0f} Pa\n"
        f"⛰高度: {alt:.2f} m\n"
        f"{advice}"
    )

    # ---- LINE送信 ----
    body = {"messages": [{"type": "text", "text": msg}]}
    try:
        requests.post(url, headers=headers, json=body, timeout=10)
        print("送信:", msg)
    except Exception as e:
        print("送信エラー:", e)

    time.sleep(600)  # 10分おき
