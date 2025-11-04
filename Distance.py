import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24
TIMEOUT_S = 0.03   # 30ms（約5m往復で ~29ms）

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def pulse_in(pin, level, timeout):
    start = time.monotonic()
    # 待機：レベル変化を待つ
    while GPIO.input(pin) != level:
        if time.monotonic() - start > timeout:
            return None
    t0 = time.monotonic()
    # パルス幅計測
    while GPIO.input(pin) == level:
        if time.monotonic() - t0 > timeout:
            return None
    t1 = time.monotonic()
    return t1 - t0

try:
    while True:
        # 10usトリガ
        GPIO.output(TRIG, False)
        time.sleep(0.00005)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)  # 10µs
        GPIO.output(TRIG, False)

        dur = pulse_in(ECHO, 1, TIMEOUT_S)
        if dur is None:
            print("timeout")
        else:
            # 音速 34300 cm/s、往復→/2
            distance_cm = dur * 34300.0 / 2.0
            print(f"{distance_cm:.1f} cm")
        time.sleep(0.2)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
