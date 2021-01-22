import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

MA1_PIN = 27
MA2_PIN = 18 #BCM pinouts
MB1_PIN = 22
MB2_PIN = 23 #BCM pinouts

freq = 1000 #PWM frequency, this drastically changes motor preformance

GPIO.setup(MA1_PIN, GPIO.OUT)
GPIO.setup(MA2_PIN, GPIO.OUT)

MA1 = GPIO.PWM(MA1_PIN, freq) 
MA2 = GPIO.PWM(MA2_PIN, freq)

GPIO.setup(MB1_PIN, GPIO.OUT)
GPIO.setup(MB2_PIN, GPIO.OUT)

MB1 = GPIO.PWM(MB1_PIN, freq) 
MB2 = GPIO.PWM(MB2_PIN, freq)

MA1.start(0)
MA2.start(0)
MB1.start(0)
MB2.start(0)

for speed in range(20, 101, 1):
    MA1.ChangeDutyCycle(0)
    MA2.ChangeDutyCycle(speed)
    MB1.ChangeDutyCycle(0)
    MB2.ChangeDutyCycle(speed)
    time.sleep(0.1)
time.sleep(2)
for speed in range(20, 101, 1):
    MA1.ChangeDutyCycle(speed)
    MA2.ChangeDutyCycle(0)
    MB1.ChangeDutyCycle(speed)
    MB2.ChangeDutyCycle(0)
    time.sleep(0.1)
time.sleep(2)

MA1.stop()
MA2.stop()
MB1.stop()
MB2.stop()
GPIO.cleanup()



