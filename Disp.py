# lcd_text.py
# Raspberry Pi Zero W + 1602A（I2Cなし・並列接続）
# 任意の文字列をLCDに表示

from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time
import sys

# === LCD設定（BOARD番号で指定） ===
lcd = CharLCD(
    cols=16, rows=2,
    pin_rs=37, pin_e=35,
    pins_data=[33, 31, 29, 23],  # D4, D5, D6, D7
    numbering_mode=GPIO.BOARD,
    charmap='A00'
)

def show_text(line1="", line2=""):
    """LCDの1行目と2行目に文字列を表示"""
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1[:16])  # 16文字まで
    if line2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2[:16])

try:
    # コマンドライン引数で文字を受け取る
    args = sys.argv[1:]
    if len(args) == 0:
        show_text("Hello, world!", "from Pi Zero W")
    elif len(args) == 1:
        show_text(args[0])
    else:
        show_text(args[0], args[1])

    # 表示を維持
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()
