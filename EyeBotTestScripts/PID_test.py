import time
from simple_pid import PID
from EncoderCounter import Counter
from MotorDriver import MotorDriver


counter = Counter()
drive = MotorDriver()

pid = PID(0.09, 0.01, 0.06, setpoint=1*894*1)
pid.output_limits = (-100, 100) #multiply for better precision
counter.clear()
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
    counter.update_data()
    
    #ENCODER B
    true_B_count = counter.get_B()
    counterB += direction * (true_B_count - last_true_count_B)
    dB = counterB - last_count_B
    last_true_count_B = true_B_count
    last_count_B = counterB
    
    #ENCODER A
    counterA = counter.get_A()
    

    output = pid(counterB)
    print("Counter A: %d,  Counter B: %d,  Speed: %d, dE/dT: %d, Setpoint: %d, Direction: %d" % (counterA, counterB, output, dB, pid.setpoint, direction))
    
    if(passed and once):
        if(last_dB < dB and dB < 8): #direction reversed
            direction *= -1
            #passed = False
            #once = False
        else:
            last_dB = dB
    
    
    if(counterB > pid.setpoint and not passed):
        passed = True
        last_dB = dB
        #now track derivitive to find motor turning point
        
    drive.set_speed(output, output)
