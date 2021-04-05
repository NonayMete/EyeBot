import time
from simple_pid import PID

#import simple_pid
from EncoderCounter import Counter
from MotorDriver import MotorDriver


counter = Counter()
drive = MotorDriver()

distance = 0.25 #meters

distance /= 0.07*3.1415926 #rotations needed
distance *= 894 #counts needed

pidA = PID(0.12, 0.001, 0.06, setpoint=distance)
pidA.output_limits = (0, 100) #multiply for better precision
pidA.sample_time = 0.01

pidB = PID(0.12, 0.001, 0.06, setpoint=distance)
pidB.output_limits = (0, 100) #multiply for better precision
pidB.sample_time = 0.01

counter.clear()

while 1:
    counter.update_data()
    
    #ENCODER A
    counterA = counter.get_A()
    outputA = pidA(counterA)
    
    #ENCODER B
    counterB = counter.get_B()
    outputB = pidB(counterB)
    
    print("Counter A: %d,  Counter B: %d,  SpeedA: %d,  SpeedB: %d,  Setpoint: %d" % (counterA, counterB, outputA, outputB, pidA.setpoint))

    drive.set_speed(outputA, outputB)

