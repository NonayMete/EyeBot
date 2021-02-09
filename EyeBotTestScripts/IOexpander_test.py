import smbus
import time
from IOexpander import PCF8574
#from pcf8574 import PCF8574
#this class is a library that can just be imported too


i2c_port_num = 1 #I2C bus 1 on the pi
pcf_address = 0x20 #default I2C address, for the PCF controlling distance sensors #U7
pcf1 = PCF8574(i2c_port_num, pcf_address)

pcf_address = 0x27 #U4
pcf2 = PCF8574(i2c_port_num, pcf_address)

pcf_address = 0x21 #U1
pcf3 = PCF8574(i2c_port_num, pcf_address)


#pcf3.port = [True, True, True, True, True, True, True, True] #set ports as list P0-7
pcf3.port = [False, False, False, False, False, False, False, False]
#pcf1.port[7] = True #or individually
#print(pcf1.port[0]) #returns state of port
while 1:
    #print(pcf1.port) #returns state of P0-7 as a list
    print(pcf3.port)
    time.sleep(2)
