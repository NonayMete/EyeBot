import time
from EncoderCounter import Counter
counter = Counter()

while 1:
    counter.update_data()
    #GBL()
    #print(data.port)
    Acount = counter.get_A()
    Bcount = counter.get_B()
    print("Counter A: %d,  Counter B: %d" % (Acount, Bcount))
    #print("Counter B: %d" % (get_counter_B()))
    time.sleep(1)

