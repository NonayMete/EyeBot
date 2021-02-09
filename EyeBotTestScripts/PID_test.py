import smbus
from IOexpander import PCF8574
import RPi.GPIO as GPIO
import time
from simple_pid import PID

def clear_counters():
    control.port[3] = False
    control.port[3] = True

def update_data():
    control.port[2] = False
    control.port[2] = True
    
def GAU():
    control.port[7] = True
    control.port[6] = True
    control.port[5] = False
    control.port[4] = True
    
def GAL():
    control.port[7] = True
    control.port[6] = True
    control.port[5] = True
    control.port[4] = False
    
def GBU():
    control.port[7] = False
    control.port[6] = True
    control.port[5] = True
    control.port[4] = True
    
def GBL():
    control.port[7] = True
    control.port[6] = False
    control.port[5] = True
    control.port[4] = True
    
def get_counter_A():
    GAU()
    upper = data.port
    upper.reverse()
    n = 15
    count = 0
    for bit in upper:
        if bit:
            count += pow(2, n)
        n-=1
    GAL()
    lower = data.port
    n = 7
    for bit in lower:
        if bit:
            count += pow(2, n)
        n-=1
    return count

def get_counter_B():
    GBU()
    upper = data.port
    upper.reverse()
    n = 15
    count = 0
    for bit in upper:
        if bit:
            count += pow(2, n)
        n-=1
    GBL()
    lower = data.port
    n = 7
    for bit in lower:
        if bit:
            count += pow(2, n)
        n-=1
    return count

#def calculate_true_count_B():
    

i2c_port_num = 1 #I2C bus 1 on the pi
pcf_address = 0x27 #U4
data = PCF8574(i2c_port_num, pcf_address)
pcf_address = 0x21 #U1
control = PCF8574(i2c_port_num, pcf_address)

data.port = [True, True, True, True, True, True, True, True] #set ports as inputs
control.port = [True, True, True, True, True, True, True, True]

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

pid = PID(0.09, 0.01, 0.06, setpoint=1*894*1)
pid.output_limits = (-100, 100) #multiply for better precision
clear_counters()
output = 0.0
direction = 1
passed = False
pid.sample_time = 0.0001

last_count_B = 0
last_true_count_B = 0
last_dB = 0
counterB = 0
once = True
while 1:
    update_data()
    
    #ENCODER B
    true_B_count = get_counter_B()
    counterB += direction * (true_B_count - last_true_count_B)
    dB = counterB - last_count_B
    last_true_count_B = true_B_count
    last_count_B = counterB
    
    #ENCODER A
    counterA = get_counter_A()
    

    output = pid(counterB)
    print("Counter A: %d,  Counter B: %d,  Speed: %d, dE/dT: %d, Setpoint: %d, Direction: %d" % (counterA, counterB, output, dB, pid.setpoint, direction))
    
    if(passed and once):
        if(last_dB < dB and dB < 8): #direction reversed
            direction *= -1
            #once = False
        else:
            last_dB = dB
    
    
    if(counterB > pid.setpoint and not passed):
        passed = True
        last_dB = dB
        #now track derivitive to find motor turning point
        
        

        
    if(output < 0):
        MA1.ChangeDutyCycle(abs(output))
        MB1.ChangeDutyCycle(abs(output))
        MA2.ChangeDutyCycle(0)
        MB2.ChangeDutyCycle(0)
    else: #backwards
        MA2.ChangeDutyCycle(abs(output))
        MB2.ChangeDutyCycle(abs(output))
        MA1.ChangeDutyCycle(0)
        MB1.ChangeDutyCycle(0)
    
    

clear_counters()
MA1.stop()
MA2.stop()
MB1.stop()
MB2.stop()
GPIO.cleanup()
clear_counters()
