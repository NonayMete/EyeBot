import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

p = GPIO.PWM(4, 600)
while 1:
	p.ChangeFrequency(660)
	p.start(20)
	time.sleep(1)
	p.ChangeDutyCycle(0)
	time.sleep(1)

p.stop()
GPIO.cleanup()


