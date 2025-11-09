# lcd_yen.py
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time

# ←あなたの配線（BOARD番号）のまま
lcd = CharLCD(
    cols=16, rows=2,
    pin_rs=37, pin_e=35,
    pins_data=[33, 31, 29, 23],  # D4,D5,D6,D7
    numbering_mode=GPIO.BOARD,
    charmap='A00'
)

# 自作「¥」のドット絵（5x8）
yen_char = (
    0b00100,
    0b01010,
    0b11111,
    0b00100,
    0b01110,
    0b00100,
    0b00100,
    0b00000,
)
lcd.create_char(0, yen_char)  # CGRAMスロット0番に登録

def show_yen_amount(val):
    s = f"{int(round(val)):,}"   # カンマ区切り（整数に丸め）
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(chr(0) + s) # 先頭に自作¥（chr(0)）

try:
    show_yen_amount(12345)
    lcd.cursor_pos = (1, 0)
    lcd.write_string("TOTAL")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
    GPIO.cleanup()
