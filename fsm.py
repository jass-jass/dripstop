from machine import Pin
from time import sleep
import _thread


ledr = Pin(4, Pin.OUT)
ledg = Pin(5, Pin.OUT)
button = Pin(23, Pin.IN)

def blink_green():
    while True:
        ledg.on()
        sleep(1)
        ledg.off()
        sleep(1)
        
# hardware interrupts pass a pin as an argument to the ISR
# ISR difficulty in handling core 2 resources 
# in current code, control doesn't exit ISR
def ISR_blink(int_pin):
    ledr.on()
    sleep(5)
    ledr.off()
    sleep(5)

button.irq(trigger = Pin.IRQ_RISING, handler = ISR_blink)

_thread.start_new_thread(blink_green, ())

while True:
    ledr.on()
    sleep(1)
    ledr.off()
    sleep(1)
