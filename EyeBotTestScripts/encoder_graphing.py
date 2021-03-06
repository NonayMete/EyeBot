import smbus
import RPi.GPIO as GPIO
import time
from simple_pid import PID
#from pcf8574 import PCF8574
#this class is a library that can just be imported too

class IOPort(list):
    """
    Represents the PCF8574 IO port as a list of boolean values.
    """
    def __init__(self, pcf8574, *args, **kwargs):
        super(IOPort, self).__init__(*args, **kwargs)
        self.pcf8574 = pcf8574

    def __setitem__(self, key, value):
        """
        Set an individual output pin.
        """
        self.pcf8574.set_output(key, value)

    def __getitem__(self, key):
        """
        Get an individual pin state.
        """
        return self.pcf8574.get_pin_state(key)

    def __repr__(self):
        """
        Represent port as a list of booleans.
        """
        state = self.pcf8574.bus.read_byte(self.pcf8574.address)
        ret = []
        for i in range(8):
            #ret.append(bool(state & 1<<7-i))
            ret.append(bool(state & 1<<i))
        return repr(ret)

    def __len__(self):
        return 8

    def __iter__(self):
        for i in range(8):
            yield self[i]

    def __reversed__(self):
        for i in range(8):
            yield self[7-i]


class PCF8574(object):
    """
    A software representation of a single PCF8574 IO expander chip.
    """
    def __init__(self, i2c_bus_no, address):
        self.bus_no = i2c_bus_no
        self.bus = smbus.SMBus(i2c_bus_no)
        self.address = address

    def __repr__(self):
        return "PCF8574(i2c_bus_no=%r, address=0x%02x)" % (self.bus_no, self.address)

    @property
    def port(self):
        """
        Represent IO port as a list of boolean values.
        """
        return IOPort(self)

    @port.setter
    def port(self, value):
        """
        Set the whole port using a list.
        """
        assert isinstance(value, list)
        value.reverse() #new
        assert len(value) == 8
        new_state = 0
        for i, val in enumerate(value):
            if val:
                new_state |= 1 << 7-i
        self.bus.write_byte(self.address, new_state)

    def set_output(self, output_number, value):
        """
        Set a specific output high (True) or low (False).
        """
        assert output_number in range(8), "Output number must be an integer between 0 and 7"
        current_state = self.bus.read_byte(self.address)
        #bit = 1 << 7-output_number
        bit = 1 << output_number
        new_state = current_state | bit if value else current_state & (~bit & 0xff)
        self.bus.write_byte(self.address, new_state)

    def get_pin_state(self, pin_number):
        """
        Get the boolean state of an individual pin.
        """
        assert pin_number in range(8), "Pin number must be an integer between 0 and 7"
        state = self.bus.read_byte(self.address)
        #return bool(state & 1<<7-pin_number)
        return bool(state & 1<<pin_number)


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

pid = PID(0.09, 0.01, 0.06, setpoint=1*894*2)
pid.output_limits = (-100, 100) #multiply for better precision
clear_counters()
output = 0.0
direction = 1
passed = False
pid.sample_time = 0.0001
last = 0
speed = 100
while 1:
    update_data()
    counterB = get_counter_B()
    counterA = get_counter_A()
    dCount =  counterB - last
    last = counterB
    print("Counter A: %d,  Counter B: %d,  Speed: %d, dE/dT: %d, Setpoint: %d" % (counterA, counterB, output, dCount, pid.setpoint))
    
    if(speed > 0):
        MA1.ChangeDutyCycle(0)
        MA2.ChangeDutyCycle(speed)
        MB1.ChangeDutyCycle(0)
        MB2.ChangeDutyCycle(speed)
    else:
        MA1.ChangeDutyCycle(abs(speed))
        MA2.ChangeDutyCycle(0)
        MB1.ChangeDutyCycle(abs(speed))
        MB2.ChangeDutyCycle(0)
    #time.sleep(2)
    time.sleep(0.01)    
    speed -= 1

clear_counters()
MA1.stop()
MA2.stop()
MB1.stop()
MB2.stop()
GPIO.cleanup()
clear_counters()

