from machine import Pin
from time import sleep

ledr = Pin(4, Pin.OUT)
ledg = Pin(5, Pin.OUT)
button = Pin(23, Pin.IN)

def blink_green():
    while True:
        ledg.on()
        sleep(1)
        ledg.off()
        sleep(1)
        
def ISR_blink():
    while True:
        ledg.on()
        sleep(2)
        ledg.off()
        sleep(2)

button.irq(trigger = Pin.IRQ_RISING, handler = ISR_blink)

_thread.start_new_thread(blink_green, ())

while True:
    ledr.on()
    sleep(1)
    ledr.off()
    sleep(1)
