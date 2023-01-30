from machine import Pin
from time import sleep
import _thread

led_green = Pin(18, Pin.OUT)
led_red = Pin(23, Pin.OUT)
led_white = Pin(4, Pin.OUT)

def led_white_thread():
    while True:
        led_white.value(1)
        sleep(5)
        led_white.value(0)
        sleep(5)
    
_thread.start_new_thread(led_white_thread, ())

while True:
    led_green.value(1)
    sleep(1)
    led_red.value(1)
    sleep(2)
    led_red.value(0)
    sleep(1)
    led_green.value(0)
    sleep(1)
