import time
from MotorDriver import MotorDriver
        
drive = MotorDriver()

for speed in range(20, 101, 1):
    drive.set_speed(speed, speed)
    time.sleep(0.01)
#time.sleep(2)
for speed in range(20, 101, 1):
    drive.set_speed(-speed, -speed)
    time.sleep(0.01)
#time.sleep(2)

drive.stop()


