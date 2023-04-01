from machine import Pin, I2C
import sh1106


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
print(addr)


i2c = I2C(0)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(2), addr[0], rotate=0, delay=0)
display.sleep(False)
display.fill(0)
display.text('Testing 1', 0, 0, 1)
display.show()
