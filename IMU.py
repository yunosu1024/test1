from mpu6050 import mpu6050
import time

# I2Cアドレス (i2cdetectで68が出ていたので0x68)
sensor = mpu6050(0x68)

while True:
    accel = sensor.get_accel_data()   # 加速度 [m/s²]
    gyro  = sensor.get_gyro_data()    # 角速度 [°/s]
    temp  = sensor.get_temp()         # 温度 [°C]

    print(f"Accel: x={accel['x']:.3f} y={accel['y']:.3f} z={accel['z']:.3f}")
    print(f"Gyro:  x={gyro['x']:.3f} y={gyro['y']:.3f} z={gyro['z']:.3f}")
    print(f"Temp:  {temp:.2f} °C")
    print("-" * 50)
    time.sleep(0.5)
