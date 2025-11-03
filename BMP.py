# bmp180_test.py
from smbus import SMBus
from bmp180 import BMP180
import time

bus = SMBus(1)
bmp = BMP180(bus)
bmp.oversample_set(3)
bmp.sea_level_pressure = 101325  

while True:
    t = bmp.temperature
    p = bmp.pressure
    alt = bmp.altitude
    print(f"Temp={t:.2f} °C  Pres={p:.0f} Pa  Alt={alt:.2f} m")
    time.sleep(1)
