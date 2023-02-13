from machine import Pin, I2C
from time import sleep

sda_pin = Pin(21, Pin.IN)
scl_pin = Pin(22, Pin.IN)
int_pin = Pin(23, Pin.IN, Pin.PULL_UP)
#data_pin = Pin(4, Pin.OUT, Pin.PULL_UP)

i2c_device = I2C(0, scl = scl_pin, sda = sda_pin)
#lcd = I2C(channel_number, scl=Pin(number), sda=Pin(number), freq=frequency)
## in case of multiple i2c channels
i2c_address = i2c_device.scan()
print(i2c_address)

#data_pin.value(1)
#buf = ''
buf = bytearray(2)

while True:
    if (not int_pin.value()):
        i2c_device.readfrom_into(i2c_address[0], buf)
        print(buf)
        sleep(1)
