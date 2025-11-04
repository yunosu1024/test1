# bmp180_test.py
from smbus2 import SMBus
from bmp180_min import BMP180
import time

bus = SMBus(1)                # I2C bus 1
bmp = BMP180(bus, address=0x77, oversample=3)
bmp.sea_level_pressure = 101325   

while True:
    t = bmp.temperature
    p = bmp.pressure
    alt = bmp.altitude
    print(f"Temp={t:.2f} degree  Pres={p:.0f} Pa  Alt={alt:.2f} m")
    time.sleep(1)
