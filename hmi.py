import machine
import pcf8574
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)
int_pcf = Pin(23, Pin.IN)

I2C_ADDR = i2c.scan()
print(I2C_ADDR)
totalRows = 4
totalColumns = 20

lcd = I2cLcd(i2c, I2C_ADDR[1], totalRows, totalColumns)
pcf = pcf8574.PCF8574(i2c, I2C_ADDR[0])

data = []


def poll(s):
    global data
    arr = []
    ones = 0
    print('irq')
    for i in range(8):
        temp = pcf.pin(i)
        print(temp)
        arr.append(temp)
        if temp:
            ones = ones + 1
    print(ones)
    if ones != 7:
        return
    data = arr
    print(data)


int_pcf.irq(trigger = Pin.IRQ_FALLING, handler = poll)

while True:
    lcd.move_to(0,0)
    lcd.putstr(str(data))
