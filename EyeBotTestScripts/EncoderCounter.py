import smbus
import time
from IOexpander import PCF8574

class Counter:
    
    def __init__(self):
        i2c_port_num = 1 #I2C bus 1 on the pi
        pcf_address = 0x27 #U4
        self.data = PCF8574(i2c_port_num, pcf_address)
        pcf_address = 0x21 #U1
        self.control = PCF8574(i2c_port_num, pcf_address)
        self.data.port = [True, True, True, True, True, True, True, True] #set ports as inputs
        self.control.port = [True, True, True, True, True, True, True, True]
        self.clear()
        
    def clear(self):
        self.control.port[3] = False
        self.control.port[3] = True

    def update_data(self):
        self.control.port[2] = False
        self.control.port[2] = True
    
    def GAU(self):
        self.control.port[7] = True
        self.control.port[6] = True
        self.control.port[5] = False
        self.control.port[4] = True
    
    def GAL(self):
        self.control.port[7] = True
        self.control.port[6] = True
        self.control.port[5] = True
        self.control.port[4] = False
    
    def GBU(self):
        self.control.port[7] = False
        self.control.port[6] = True
        self.control.port[5] = True
        self.control.port[4] = True
    
    def GBL(self):
        self.control.port[7] = True
        self.control.port[6] = False
        self.control.port[5] = True
        self.control.port[4] = True
    
    def get_A(self):
        self.GAU()
        upper = self.data.port
        upper.reverse()
        n = 15
        count = 0
        for bit in upper:
            if bit:
                count += pow(2, n)
            n-=1
        self.GAL()
        lower = self.data.port
        n = 7
        for bit in lower:
            if bit:
                count += pow(2, n)
            n-=1
        return count

    def get_B(self):
        self.GBU()
        upper = self.data.port
        upper.reverse()
        n = 15
        count = 0
        for bit in upper:
            if bit:
                count += pow(2, n)
            n-=1
        self.GBL()
        lower = self.data.port
        n = 7
        for bit in lower:
            if bit:
                count += pow(2, n)
            n-=1
        return count
