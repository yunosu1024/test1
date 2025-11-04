# bmp180_min.py
# Minimal BMP180 driver (Bosch datasheet formula) using smbus2 only.
from time import sleep
from smbus2 import SMBus
import math

class BMP180:
    def __init__(self, bus: SMBus, address=0x77, oversample=3):
        self.bus = bus
        self.address = address
        self.oversample = max(0, min(3, oversample))
        self._read_calibration()
        self.sea_level_pressure = 101325  # Pa

    def _readS16(self, reg):
        b = self.bus.read_i2c_block_data(self.address, reg, 2)
        v = (b[0] << 8) | b[1]
        return v - 65536 if v & 0x8000 else v

    def _readU16(self, reg):
        b = self.bus.read_i2c_block_data(self.address, reg, 2)
        return (b[0] << 8) | b[1]

    def _read_calibration(self):
        self.AC1 = self._readS16(0xAA)
        self.AC2 = self._readS16(0xAC)
        self.AC3 = self._readS16(0xAE)
        self.AC4 = self._readU16(0xB0)
        self.AC5 = self._readU16(0xB2)
        self.AC6 = self._readU16(0xB4)
        self.B1  = self._readS16(0xB6)
        self.B2  = self._readS16(0xB8)
        self.MB  = self._readS16(0xBA)
        self.MC  = self._readS16(0xBC)
        self.MD  = self._readS16(0xBE)

    def _read_raw_temp(self):
        self.bus.write_byte_data(self.address, 0xF4, 0x2E)
        sleep(0.005)  # 4.5ms
        msb, lsb = self.bus.read_i2c_block_data(self.address, 0xF6, 2)
        return (msb << 8) | lsb  # UT

    def _read_raw_press(self):
        oss = self.oversample
        self.bus.write_byte_data(self.address, 0xF4, 0x34 + (oss << 6))
        # Max conversion time: 4.5/7.5/13.5/25.5 ms
        sleep([0.005, 0.008, 0.014, 0.026][oss])
        msb, lsb, xlsb = self.bus.read_i2c_block_data(self.address, 0xF6, 3)
        up = ((msb << 16) | (lsb << 8) | xlsb) >> (8 - oss)
        return up  # UP

    def _compute_b5(self, UT):
        X1 = ((UT - self.AC6) * self.AC5) >> 15
        X2 = (self.MC << 11) // (X1 + self.MD)
        return X1 + X2  # B5

    @property
    def temperature(self):
        UT = self._read_raw_temp()
        B5 = self._compute_b5(UT)
        T = (B5 + 8) >> 4  # 0.1‹C
        return T / 10.0

    @property
    def pressure(self):
        UT = self._read_raw_temp()
        UP = self._read_raw_press()
        B5 = self._compute_b5(UT)

        oss = self.oversample
        B6 = B5 - 4000
        X1 = (self.B2 * ((B6 * B6) >> 12)) >> 11
        X2 = (self.AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.AC1 * 4 + X3) << oss) + 2) >> 2
        X1 = (self.AC3 * B6) >> 13
        X2 = (self.B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> oss)

        if B7 < 0x80000000:
            p = (B7 * 2) // B4
        else:
            p = (B7 // B4) * 2

        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        p = p + ((X1 + X2 + 3791) >> 4)
        return int(p)  # Pa

    @property
    def altitude(self):
        p = self.pressure
        p0 = float(self.sea_level_pressure)
        # ŒöŽ®: h = 44330 * (1 - (p/p0)^(1/5.255))
        return 44330.0 * (1.0 - pow(p / p0, 1.0 / 5.255))

    def oversample_set(self, n):
        self.oversample = max(0, min(3, int(n)))
