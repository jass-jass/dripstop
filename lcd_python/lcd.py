import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

I2C_ADDR = 0x27
totalRows = 4
totalColumns = 20

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

while True:
    lcd.putstr("LCD using I2C")
    sleep(2)
    lcd.move_to(0, 1)
    lcd.putstr("Lets Count")
    sleep(2)
    for i in range(11):
        lcd.move_to(i, 2)
        lcd.putstr(str(i))
        sleep(1)
    lcd.move_to(0, 3)
    lcd.putstr("End")
    sleep(5)
    lcd.clear()
