from machine import Pin
from time import sleep
import _thread

led = Pin(4, Pin.OUT)
button = Pin(23, Pin.IN)

button_status = False

def read_button():
    global button_status
    while True:
        button_status = button.value()
    
_thread.start_new_thread(read_button, ())

while True:
    led.value(button_status)
