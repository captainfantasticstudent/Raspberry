import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

pwm = GPIO.PWM(4, 1)
pwm.start(50)

time.sleep(1)

pwm.stop()

GPIO.cleanup()
