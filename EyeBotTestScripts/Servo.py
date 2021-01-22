from gpiozero import Servo
from time import sleep

myCorrection=0
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
 
servo1 = Servo(5,min_pulse_width=minPW,max_pulse_width=maxPW)
servo2 = Servo(6,min_pulse_width=minPW,max_pulse_width=maxPW)
servo3 = Servo(12,min_pulse_width=minPW,max_pulse_width=maxPW)
servo4 = Servo(13,min_pulse_width=minPW,max_pulse_width=maxPW)
while True:
 
  print("Set value range -1.0 to +1.0")
  for value in range(0,21):
    value2=(float(value)-10)/10
    servo1.value=value2
    servo2.value=value2
    servo3.value=value2
    servo4.value=value2    
    print(value2)
    sleep(0.5)
 
  print("Set value range +1.0 to -1.0")
  for value in range(20,-1,-1):
    value2=(float(value)-10)/10
    servo1.value=value2
    servo2.value=value2
    servo3.value=value2
    servo4.value=value2
    print(value2)
    sleep(0.5)
