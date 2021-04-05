import time
from simple_pid import PID
from EncoderCounter import Counter
from MotorDriver import MotorDriver

class DrivePID():
    def __init__(self, P, I, D):
        
        
        
counter = Counter()
drive = MotorDriver()

pidA = PID(0.12, 0.0, 0.05, setpoint=1*894*1)
#pid = PID(0.1, 0, 0, setpoint=1*894*1)
pidA.output_limits = (-100, 100) #multiply for better precision
pidA.sample_time = 0.001

pidB = PID(0.12, 0.0, 0.05, setpoint=1*894*1)
#pid = PID(0.1, 0, 0, setpoint=1*894*1)
pidB.output_limits = (-100, 100) #multiply for better precision
pidB.sample_time = 0.001
counter.clear()

outputA = 0.0
outputB = 0.0
directionA = 1
directionB = 1
passedA = False
passedB = False

last_count_B = 0
last_true_count_B = 0
last_dB = 0
counterB = 0

last_count_A = 0
last_true_count_A = 0
last_dA = 0
counterA = 0

once = True
while 1:
    counter.update_data()
    
    #ENCODER B
    true_B_count = counter.get_B()
    counterB += directionB * (true_B_count - last_true_count_B)
    dB = counterB - last_count_B
    last_true_count_B = true_B_count
    last_count_B = counterB
    
    #ENCODER A
    true_A_count = counter.get_A()
    counterA += directionA * (true_A_count - last_true_count_A)
    dA = counterA - last_count_A
    last_true_count_A = true_A_count
    last_count_A = counterA
    
    #if(direction == -1):
    #    GPIO.output(19, True)
    #else:
    #    GPIO.output(19, False)
    
    if(passedA and once):
        if(last_dA < dA and dA < 8): #direction reversed
            directionA *= -1
            #GPIO.output(19, True)
            passedA = False
            #once = False
            
    if(passedB and once):
        if(last_dB < dB and dB < 8): #direction reversed
            directionB *= -1
            #GPIO.output(19, True)
            passedB = False
            #once = False
        
    if(directionA == 1):
        if(counterA > pidA.setpoint and not passedA):
            passedA = True
            last_dA = dA
            #now track derivitive to find motor turning point
    else:
        if(counterA < pidA.setpoint and not passedA):
            passedA = True
            last_dA = dA
            
    if(directionB == 1):
        if(counterB > pidB.setpoint and not passedB):
            passedB = True
            last_dB = dB
            #now track derivitive to find motor turning point
    else:
        if(counterB < pidB.setpoint and not passedB):
            passedB = True
            last_dB = dB
            
    outputA = pidA(counterA)         
    outputB = pidB(counterB)
    #print("Counter A: %d,  Counter B: %d,  Speed: %d, dB: %d, last dB: %d, Setpoint: %d, Direction: %d, Passed: %d" % (counterA, counterB, output, dB, last_dB, pid.setpoint, direction, passed))
    last_dB = dB
    last_dA = dA
    drive.set_speed(outputA, outputB)

