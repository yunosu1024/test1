from smbus2 import SMBus
from bmp180_min import BMP180
import requests, time
from datetime import datetime, timedelta, timezone

# 日本時間（UTC+9）
JST = timezone(timedelta(hours=9))

TOKEN = "3aOkPW3pzGhHqSR0gPOofifBDM8kMRAVZneAmE8bYEUcxh1fLxsOX8ReMWXVOAsfFGvsyKpRziU54PIG56"
url = "https://api.line.me/v2/bot/message/broadcast"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

bus = SMBus(1)
bmp = BMP180(bus, address=0x77, oversample=3)
bmp.sea_level_pressure = 101325

while True:
    now = datetime.now(JST)
    time_str = now.strftime("%Y-%m-%d %H:%M")

    t = bmp.temperature
    p = bmp.pressure
    alt = bmp.altitude

    advice = ""

    if t >= 30:
        advice += "🥵 暑さに注意！こまめに水分補給を。\n"
    elif 20 <= t < 30:
        advice += "🌼 過ごしやすい気温ですね。良い一日を！\n"
    elif 10 <= t < 20:
        advice += "🍂 少し肌寒いです。軽く羽織ると快適です。\n"
    elif 0 <= t < 10:
        advice += "🥶 朝晩は冷え込みます。暖かくして過ごしましょう。\n"
    else:
        advice += "❄️ とても寒いです。防寒対策をしっかり！\n"

    if p <= 100500:
        advice += "🌧 低気圧傾向です。体調や頭痛に気を付けて。\n"
    elif p >= 102500:
        advice += "🌤 高気圧です。気分も晴れやかにいきましょう。\n"
    else:
        advice += "🌥 安定した気圧です。穏やかな日になりそうです。\n"

    msg = (
        f"⏰ 時刻: {time_str}（日本時間）\n"
        f"🌡 温度: {t:.2f} ℃\n"
        f"🧭 気圧: {p:.0f} Pa\n"
        f"{advice}"
    )

    body = {"messages": [{"type": "text", "text": msg}]}
    try:
        res = requests.post(url, headers=headers, json=body, timeout=10)
        print(f"[{time_str}] 送信完了 ({res.status_code})")
    except Exception as e:
        print("送信エラー:", e)

    time.sleep(600)
