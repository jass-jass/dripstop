from machine import Pin
from time import sleep
import _thread

led = Pin(4, Pin.OUT)
#pulse = Pin(18, Pin.OUT)
button = Pin(23, Pin.IN)

button_status = False

def read_button():
    global button_status
    while True:
        button_status = button.value()
    
def handle_interrupt(Pin):
    _thread.exit()
    print("reset in")
    for i in range(10):
        print("\n", i)
        sleep(1)
    
_thread.start_new_thread(read_button, ())

Interrupt = Pin(0,Pin.IN)
Interrupt.irq(trigger=Pin.IRQ_FALLING, handler = handle_interrupt)

while True:
    led.value(button_status)
