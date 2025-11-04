from smbus2 import SMBus
from bmp180_min import BMP180
import requests, time
from datetime import datetime

# === LINE設定 ===
TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"   # ← あなたのトークンを貼る
url = "https://api.line.me/v2/bot/message/broadcast"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# === BMP180設定 ===
bus = SMBus(1)
bmp = BMP180(bus, address=0x77, oversample=3)
bmp.sea_level_pressure = 101325

# === メインループ ===
while True:
    # 現在時刻（日本時間）
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")

    # センサー値取得
    t = bmp.temperature
    p = bmp.pressure
    alt = bmp.altitude

    # ---- 条件付きメッセージ生成 ----
    advice = ""

    # 温度による季節・体感コメント
    if t >= 30:
        advice += "🥵 暑さに注意！こまめな水分補給を。\n"
    elif 20 <= t < 30:
        advice += "🌼 過ごしやすい気温ですね。良い一日を！\n"
    elif 10 <= t < 20:
        advice += "🍂 少し肌寒いです。軽く羽織ると快適です。\n"
    elif 0 <= t < 10:
        advice += "🥶 朝晩は冷え込みます。暖かくして過ごしましょう。\n"
    else:  # 氷点下
        advice += "❄️ とても寒いです。防寒対策をしっかり！\n"

    # 気圧コメント
    if p <= 100500:
        advice += "🌧 低気圧傾向です。体調や頭痛に気を付けて。\n"
    elif p >= 102500:
        advice += "🌤 高気圧です。気分も晴れやかにいきましょう。\n"
    else:
        advice += "🌥 安定した気圧です。穏やかな日になりそうです。\n"

    # ---- 本文メッセージ ----
    msg = (
        f"⏰ 時刻: {time_str}\n"
        f"🌡 温度: {t:.2f} ℃\n"
        f"🧭 気圧: {p:.0f} Pa\n"
        f"⛰ 高度: {alt:.2f} m\n\n"
        f"{advice}"
    )

    # ---- LINE送信 ----
    body = {"messages": [{"type": "text", "text": msg}]}
    try:
        res = requests.post(url, headers=headers, json=body, timeout=10)
        print(f"[{time_str}] 送信完了 ({res.status_code})")
        print(msg)
    except Exception as e:
        print("送信エラー:", e)

    time.sleep(600)  # 10分おき
