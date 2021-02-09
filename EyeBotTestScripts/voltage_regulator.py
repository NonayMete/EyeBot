import smbus
import time

bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x4D  # default address
t = 0
while True:
    # Reads word (2 bytes) as int
    rd = bus.read_word_data(i2c_address, 0)
    # Exchanges high and low bytes
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
    data = data >> 2
    data = float(data) / 1024 #fraction of max voltage (5V)
    data *= 5.0 #voltage entering Ain Pin
    data /= 0.319728 #voltage entering ADC is put through devider, this gives us battery voltage
    data *= 1.0 #error cancellation
    data = round(data, 2) #only 2 decimal places
    t = round(t,1)
    print(t, "s:", data)
    t += 0.1
    time.sleep(0.1)

