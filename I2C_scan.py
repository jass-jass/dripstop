from machine import Pin, I2C
import time

lcd = I2C(0)
#lcd = I2C(channel_number, scl=Pin(number), sda=Pin(number), freq=frequency)
## in case of multiple i2c channels
print(lcd.scan())
