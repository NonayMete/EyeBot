import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)

for i in range(50):
	GPIO.output(19, True)
	time.sleep(1)
	GPIO.output(19, False)
	time.sleep(1)
GPIO.cleanup()

