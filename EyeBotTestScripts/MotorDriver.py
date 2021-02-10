import RPi.GPIO as GPIO

class MotorDriver:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.MA1_PIN = 27
        self.MA2_PIN = 18 #BCM pinouts
        self.MB1_PIN = 22
        self.MB2_PIN = 23 #BCM pinouts
        freq = 1000 #PWM frequency, this drastically changes motor preformance
        GPIO.setup(self.MA1_PIN, GPIO.OUT)
        GPIO.setup(self.MA2_PIN, GPIO.OUT)
        self.MA1 = GPIO.PWM(self.MA1_PIN, freq) 
        self.MA2 = GPIO.PWM(self.MA2_PIN, freq)
        GPIO.setup(self.MB1_PIN, GPIO.OUT)
        GPIO.setup(self.MB2_PIN, GPIO.OUT)
        self.MB1 = GPIO.PWM(self.MB1_PIN, freq) 
        self.MB2 = GPIO.PWM(self.MB2_PIN, freq)
        self.MA1.start(0)
        self.MA2.start(0)
        self.MB1.start(0)
        self.MB2.start(0)
        
    def stop(self):
        self.MA1.ChangeDutyCycle(0)
        self.MA2.ChangeDutyCycle(0)
        self.MB1.ChangeDutyCycle(0)
        self.MB2.ChangeDutyCycle(0)
    
    def setA(self, speed):
        if(speed > 0):
            self.MA1.ChangeDutyCycle(abs(speed))
            self.MA2.ChangeDutyCycle(0)
        else:
            self.MA1.ChangeDutyCycle(0)
            self.MA2.ChangeDutyCycle(abs(speed))
            
    def setB(self, speed):
        if(speed > 0):
            self.MB1.ChangeDutyCycle(abs(speed))
            self.MB2.ChangeDutyCycle(0)
        else:
            self.MB1.ChangeDutyCycle(0)
            self.MB2.ChangeDutyCycle(abs(speed))
            
    def set_speed(self, A, B):
        self.setA(A)
        self.setB(B)


