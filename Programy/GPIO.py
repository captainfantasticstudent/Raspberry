import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
#pwm = GPIO.PWM(4, 1)
#pwm.start(50)
#time.sleep(1)
#pwm.stop()

time.sleep(1)

GPIO.output(4, 1)
time.sleep(10)
GPIO.output(4, 0)

GPIO.cleanup()
