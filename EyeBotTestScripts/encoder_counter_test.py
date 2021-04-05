import time
from EncoderCounter import Counter
from MotorDriver import MotorDriver
counter = Counter()
drive = MotorDriver()
#drive.set_speed(2, 2)
while 1:
    counter.update_data()
    #GBL()
    #print(data.port)
    Acount = counter.get_A()
    Bcount = counter.get_B()
    print("Counter A: %d,  Counter B: %d" % (Acount, Bcount))
    #print("Counter B: %d" % (get_counter_B()))
    time.sleep(1)

