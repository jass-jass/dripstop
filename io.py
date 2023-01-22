from machine import Pin
import time

# pin definitions
led = Pin(2, Pin.OUT)
but = Pin(0, Pin.IN)
out = Pin(15, Pin.OUT)


def loop():
    #initialize
    led_val = 1
    but_val = 0
    # start time for individual pins
    led_start = 0
    but_start = 0
    out_start = 0
    
    while True:
        time_now = time.time_us()
        print (time_now)
        if (time_now - led_start > 1):
            print ("led val loop")
            led.value(led_val)
            led_start = time_now
            led_val = not led_val
        if (time_now - but_start > 1):
            but_val = but.value()
            but_start = time_now
        if (time_now - out_start > 1):
            out.value(but_val)
            out_start = time_now

loop()
