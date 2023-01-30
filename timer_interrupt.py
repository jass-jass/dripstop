from machine import Timer, Pin
from time import sleep

led_green = Pin(18, Pin.OUT)
led_white = Pin(4, Pin.OUT)

def sos_white(s):
    for i in range(3):
        led_white.value(1)
        sleep(0.5)
        led_white.value(0)
        sleep(0.5)
    for i in range(3):
        led_white.value(1)
        sleep(1)
        led_white.value(0)
        sleep(0.5)

def sos_green(s):
    for i in range(3):
        led_green.value(1)
        sleep(0.5)
        led_green.value(0)
        sleep(0.5)
    for i in range(3):
        led_green.value(1)
        sleep(1)
        led_green.value(0)
        sleep(0.5)

tim0 = Timer(0)
tim0.init(period=1000, mode=Timer.PERIODIC, callback=sos_green)

tim1 = Timer(1)
tim1.init(period=1500, mode=Timer.PERIODIC, callback=sos_white)
