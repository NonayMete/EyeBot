import smbus
import time
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
